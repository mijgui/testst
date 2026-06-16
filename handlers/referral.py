from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from promocodes import load_promocodes
from keyboards import referral_keyboard, promocode_request_keyboard
from utils import safe_delete, send_main_menu
from discounts import add_discount
from states import PromoState

from aiogram.types import Message
import html

from promocodes import load_promocodes

router = Router()

@router.callback_query(F.data == "reff")
async def reff_menu(callback: CallbackQuery):
    """
    Отображает реферальное меню с персональной ссылкой пользователя.
    """
    safe = html.escape("")
    user_id = callback.from_user.id
    bot_username = (await callback.bot.get_me()).username  # получаем username бота (без @)
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    await callback.answer()  # убираем «часики» на кнопке
    await safe_delete(callback.message)  # удаляем предыдущее сообщение (чтобы не засорять чат)
    
    await callback.message.answer(
        text=(
            "✨ Реферальная система ✨\n\n"
            "Приглашайте друзей по вашей ссылке и получайте бонусы!\n\n"
            "🎁 За каждого приглашённого друга вы получаете скидку +10% (максимум 50%).\n\n"
            "🏷️ Ваш друг тоже получит приветственную скидку 20%!\n\n"
            f"Ваша реферальная ссылка:\n{safe}<blockquote><code>{ref_link}</code></blockquote>"
        ),
        reply_markup=referral_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "promocodes")
async def promocodes_ask(callback: CallbackQuery, state: FSMContext):
    """
    Переводит пользователя в состояние ожидания ввода промокода.
    """
    await callback.answer()
    await safe_delete(callback.message)
    await state.set_state(PromoState.waiting)
    await callback.message.answer(
        text="✏️ Отправьте ваш промокод текстом.",
        reply_markup=promocode_request_keyboard()
    )

@router.message(PromoState.waiting)
async def process_promocode(message: Message, state: FSMContext):
    """
    Обрабатывает введённый промокод.
    """
    user_id = message.from_user.id
    promo_text = message.text.strip()
    found = None
    promocodes = load_promocodes()
    for promo in promocodes:
        if promo["code"].upper() == promo_text.upper():
            found = promo
            break
    if found:
        discount = found["discount"]
        add_discount(user_id, discount)
        await message.answer(f"✅ Промокод активирован! Ваша скидка {discount}%")
        await state.clear()
        await send_main_menu(message.bot, message.chat.id, user_id)
    else:
        await message.answer("❌ Неверный промокод. Попробуйте ещё раз или нажмите «Отмена».")

@router.callback_query(F.data == "cancel_promo")
async def cancel_promo_input(callback: CallbackQuery, state: FSMContext):
    """
    Отменяет ввод промокода и возвращает в главное меню.
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await callback.answer("Ввод промокода отменён.")
        await safe_delete(callback.message)
        await send_main_menu(callback.bot, callback.message.chat.id, callback.from_user.id)
    else:
        await callback.answer("Нечего отменять.")