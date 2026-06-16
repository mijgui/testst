from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import CHANNEL_USERNAME
from keyboards import subscribe_keyboard
from utils import is_subscribed, send_main_menu, safe_delete
from discounts import increase_discount, add_discount      # add_discount для приглашённого
from referral_system import set_referrer, get_referrer

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_with_ref(message: Message, command: CommandStart, state: FSMContext):
    """
    Обработка команды /start с параметром (реферальная ссылка).
    """
    await state.clear()
    user_id = message.from_user.id
    ref_arg = command.args
    referrer_id = None
    if ref_arg and ref_arg.startswith("ref_"):
        try:
            referrer_id = int(ref_arg.split("_")[1])
        except:
            pass
    # Защита: нельзя пригласить самого себя
    if referrer_id == user_id:
        referrer_id = None

    # Проверка подписки на канал
    if not await is_subscribed(message.bot, user_id, CHANNEL_USERNAME):
        # Сохраняем referrer_id в состоянии, чтобы использовать после подписки
        await state.update_data(pending_referrer=referrer_id)
        await message.answer(
            "👋 Добро пожаловать!\n\nДля использования бота подпишитесь на наш канал.",
            reply_markup=subscribe_keyboard()
        )
        return

    # Если подписка уже есть – обрабатываем реферальную логику
    await process_referral(user_id, referrer_id, message.bot, message.chat.id, user_id)
    await send_main_menu(message.bot, message.chat.id, user_id)

@router.message(CommandStart())
async def start_without_ref(message: Message, state: FSMContext):
    """
    Обработка команды /start без параметров.
    """
    await state.clear()
    if await is_subscribed(message.bot, message.from_user.id, CHANNEL_USERNAME):
        await send_main_menu(message.bot, message.chat.id, message.from_user.id)
    else:
        await message.answer(
            "👋 Добро пожаловать!\n\nДля использования бота подпишитесь на наш канал.",
            reply_markup=subscribe_keyboard()
        )

@router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery, state: FSMContext):
    """
    Проверка подписки после нажатия кнопки.
    """
    user_id = callback.from_user.id
    if await is_subscribed(callback.bot, user_id, CHANNEL_USERNAME):
        # Если была отложенная реферальная ссылка – применяем её
        data = await state.get_data()
        pending = data.get("pending_referrer")
        if pending:
            await process_referral(user_id, pending, callback.bot, callback.message.chat.id, user_id)
            await state.clear()
        await safe_delete(callback.message)
        await send_main_menu(callback.bot, callback.message.chat.id, user_id)
    else:
        await callback.answer("Вы ещё не подписаны на канал!", show_alert=True)

async def process_referral(user_id, referrer_id, bot, chat_id, from_user_id):
    """
    Обрабатывает реферальную логику:
    - Если пользователь ещё не был приглашён, то:
        * Владельцу ссылки начисляется +10% скидки (до 50%).
        * Новому пользователю начисляется приветственная скидка 20%.
    """
    if referrer_id is None:
        return
    # Проверяем, не был ли этот пользователь уже приглашён ранее
    if get_referrer(user_id):
        return  # Уже есть реферер, повторно не начисляем

    # Записываем, кто пригласил
    if set_referrer(user_id, referrer_id):
        # 1) Владельцу ссылки – +10% скидки
        new_discount_referrer = increase_discount(referrer_id, 10, 50)
        try:
            await bot.send_message(
                referrer_id,
                f"🎉 По вашей ссылке зарегистрировался новый пользователь!\n"
                f"Ваша скидка увеличена до {new_discount_referrer}%"
            )
        except:
            pass

        # 2) Приглашённому пользователю – приветственная скидка 20%
        add_discount(user_id, 20)
        await bot.send_message(
            chat_id,
            "✨ Вы перешли по реферальной ссылке!\n"
            "Вам начислена приветственная скидка 20% на первый тариф.\n"
        )