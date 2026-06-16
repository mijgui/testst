from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils import safe_edit_or_send
from keyboards import tariffs_keyboard, referral_keyboard
from navigation_manager import nav_manager, MenuLevel
import html

router = Router()


@router.callback_query(F.data == "menu:tariffs")
async def show_tariffs(callback: CallbackQuery, state: FSMContext):
    """Открыть меню тарифов"""
    await state.clear()
    user_id = callback.from_user.id
    nav_manager.push_level(user_id, MenuLevel.TARIFFS)
    
    text = "📦 Тарифы\n\n"
    await safe_edit_or_send(
        callback,
        text=text,
        reply_markup=tariffs_keyboard()
    )


@router.callback_query(F.data == "menu:referral")
async def show_referral(callback: CallbackQuery, state: FSMContext):
    """Открыть меню реферальной программы"""
    await state.clear()
    user_id = callback.from_user.id
    nav_manager.push_level(user_id, MenuLevel.REFERRAL)
    
    bot_username = (await callback.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    text = (
        "✨ Реферальная система ✨\n\n"
        "Приглашайте друзей по вашей ссылке и получайте бонусы!\n\n"
        "🎁 За каждого приглашённого друга вы получаете скидку +10% (максимум 50%).\n\n"
        "🏷️ Ваш друг тоже получит приветственную скидку 20%!\n\n"
        f"Ваша реферальная ссылка:\n<blockquote><code>{ref_link}</code></blockquote>"
    )
    
    await safe_edit_or_send(
        callback,
        text=text,
        reply_markup=referral_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "menu:join")
async def join_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки подключения (заглушка)"""
    await callback.answer("🚀 Подключение в разработке", show_alert=True)
