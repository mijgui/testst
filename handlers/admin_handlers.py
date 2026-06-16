from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS
from discounts import get_users_count
from referral_system import load_referrals
from promocodes import load_promocodes, add_promocode
from utils import safe_delete, send_main_menu

# Импортируем клавиатуры из keyboards.py (как у вас)
from keyboards import admin_keyboard, list_promo_keyboard

router = Router()

# ---------- FSM для добавления промокода ----------
class AddPromoState(StatesGroup):
    waiting_code = State()
    waiting_discount = State()

# ---------- Клавиатура отмены ----------
def cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin_cancel_promo")]]
    )

# ---------- Универсальная функция для отправки админ-панели ----------
async def send_admin_panel(target):
    """
    Отправляет админ-панель со статистикой и клавиатурой.
    target может быть Message или CallbackQuery.
    """
    # Определяем, откуда пришёл вызов
    if isinstance(target, CallbackQuery):
        user_id = target.from_user.id
        chat_id = target.message.chat.id
        await target.answer()  # убираем "часики"
    elif isinstance(target, Message):
        user_id = target.from_user.id
        chat_id = target.chat.id
    else:
        return

    if user_id not in ADMIN_IDS:
        # Если это не админ – молча игнорируем
        return

    # Собираем статистику
    users_count = get_users_count()
    referrals = load_referrals()
    referrers = set(referrals.values()) if referrals else set()
    promocodes = load_promocodes()
    text = f"📊 Статистика:\n\n"
    text += f"👥 Всего пользователей: {users_count}\n"
    text += f"🔗 Всего рефералов: {len(referrals)}\n"
    text += f"👤 Уникальных пригласивших: {len(referrers)}\n"
    text += f"🎫 Промокодов: {len(promocodes)}"

    # Отправляем сообщение с клавиатурой
    await target.bot.send_message(chat_id, text, reply_markup=admin_keyboard())

# ---------- Вход в админ-панель через команду ----------
@router.message(Command("adminp"))
async def admin_panel(message: Message):
    await send_admin_panel(message)

# ---------- Добавление промокода (начало) ----------
@router.callback_query(F.data == "admin_add_promo")
async def admin_add_promo_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещён")
        return
    await callback.answer()
    # await safe_delete(callback.message)
    await state.set_state(AddPromoState.waiting_code)
    await callback.message.edit_text(
    text="✏️ Введите код промокода (буквы/цифры):",
    reply_markup=cancel_keyboard(),
    parse_mode="Markdown")
    # await callback.message.answer(
    #     "✏️ Введите код промокода (буквы/цифры):",
    #     reply_markup=cancel_keyboard()
    # )

@router.message(AddPromoState.waiting_code)
async def admin_promo_code(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Доступ запрещён")
        await state.clear()
        return
    code = message.text.strip()
    if not code:
        await message.answer("❌ Код не может быть пустым. Попробуйте снова:")
        return
    await state.update_data(code=code)
    await state.set_state(AddPromoState.waiting_discount)
    await message.answer(
        "✏️ Введите размер скидки (число от 1 до 100):",
        reply_markup=cancel_keyboard()
    )

@router.message(AddPromoState.waiting_discount)
async def admin_promo_discount(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Доступ запрещён")
        await state.clear()
        return
    try:
        discount = int(message.text.strip())
        if discount < 1 or discount > 100:
            raise ValueError
    except:
        await message.answer("❌ Введите целое число от 1 до 100.")
        return
    data = await state.get_data()
    code = data.get("code")
    if add_promocode(code, discount):
        await message.answer(f"✅ Промокод {code} добавлен со скидкой {discount}%")
    else:
        await message.answer(f"❌ Промокод {code} уже существует.")
    await state.clear()
    # Возвращаемся в главное меню (можно заменить на админ-панель, если нужно)
    await send_main_menu(message.bot, message.chat.id, message.from_user.id)

@router.callback_query(F.data == "admin_cancel_promo")
async def admin_cancel_promo(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещён")
        return
    await state.clear()
    await callback.answer("Добавление промокода отменено.")
    await safe_delete(callback.message)
    # Возвращаемся в админ-панель со статистикой
    await send_admin_panel(callback)

# ---------- Показать список промокодов ----------
@router.callback_query(F.data == "admin_list_promos")
async def admin_list_promos(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещён")
        return
    promocodes = load_promocodes()
    if not promocodes:
        text = "📭 Список промокодов пуст."
    else:
        text = "📋 *Список промокодов:*\n\n"
        for promo in promocodes:
            text += f"→ `{promo['code']}` – {promo['discount']}%\n"
    await callback.answer()
    await safe_delete(callback.message)
    await callback.message.answer(
        text,
        reply_markup=list_promo_keyboard(),
        parse_mode="Markdown"
    )
    # await callback.message.edit_text(
    # text=text,
    # reply_markup=list_promo_keyboard(),
    # parse_mode="Markdown")

@router.callback_query(F.data == "obr_panel")
async def obr_panel(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещён")
        return
    await send_admin_panel(callback)
    print("back_panel вызван")
