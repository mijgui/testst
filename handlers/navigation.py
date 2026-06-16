from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils import safe_edit_or_send, send_main_menu
from keyboards import main_menu_keyboard, account_keyboard, tariffs_keyboard, referral_keyboard
from discounts import get_discount
from navigation_manager import nav_manager, MenuLevel
import html

router = Router()


@router.callback_query(F.data == "back")
async def back_button(callback: CallbackQuery, state: FSMContext):
    """
    Универсальная кнопка "Назад" - работает из любого места.
    Возвращает пользователя на предыдущий уровень меню.
    """
    await state.clear()
    user_id = callback.from_user.id
    current_level = nav_manager.get_current_level(user_id)
    parent_level = nav_manager.get_parent_level(current_level)
    
    # Переходим на родительский уровень
    nav_manager.pop_level(user_id)
    
    # Отображаем соответствующее меню
    if parent_level == MenuLevel.MAIN:
        discount = get_discount(user_id)
        if discount:
            text = f"🏠 Главное меню\n\n🎉 Ваша активная скидка: {discount}%"
        else:
            text = "🏠 Главное меню"
        await safe_edit_or_send(callback, text=text, reply_markup=main_menu_keyboard())
    elif parent_level == MenuLevel.ACCOUNT:
        discount = get_discount(user_id)
        safe = html.escape("")
        text = f"👤 Личный кабинет\n\n"
        text += "┌ инфа про активный тариф\n"
        text += "└ Осталось дней: \n\n"
        text += f"🎁 Активная скидка: {discount}%\n\n"
        text += f"{safe}<blockquote>👥 Получай 10% скидки за каждого приглашенного друга. Подробнее по кнопке 'Реферальная программа'</blockquote>"
        await safe_edit_or_send(callback, text=text, reply_markup=account_keyboard())
    elif parent_level == MenuLevel.TARIFFS:
        text = "📦 Тарифы\n\n"
        await safe_edit_or_send(callback, text=text, reply_markup=tariffs_keyboard())
    elif parent_level == MenuLevel.REFERRAL:
        bot_username = (await callback.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        text = (
            "✨ Реферальная система ✨\n\n"
            "Приглашайте друзей по вашей ссылке и получайте бонусы!\n\n"
            "🎁 За каждого приглашённого друга вы получаете скидку +10% (максимум 50%).\n\n"
            "🏷️ Ваш друг тоже получит приветственную скидку 20%!\n\n"
            f"Ваша реферальная ссылка:\n<blockquote><code>{ref_link}</code></blockquote>"
        )
        await safe_edit_or_send(callback, text=text, reply_markup=referral_keyboard(), parse_mode="HTML")
    else:
        discount = get_discount(user_id)
        if discount:
            text = f"🏠 Главное меню\n\n🎉 Ваша активная скид��а: {discount}%"
        else:
            text = "🏠 Главное меню"
        await safe_edit_or_send(callback, text=text, reply_markup=main_menu_keyboard())


@router.message(F.text == "👤 Личный кабинет")
async def account_message_handler(message: Message, state: FSMContext):
    """
    Обработка кнопки личного кабинета из reply-клавиатуры.
    Работает из любого места благодаря reply-кнопке.
    """
    await state.clear()
    user_id = message.from_user.id
    nav_manager.reset_history(user_id)
    nav_manager.push_level(user_id, MenuLevel.ACCOUNT)
    
    discount = get_discount(user_id)
    safe = html.escape("")
    
    text = f"👤 Личный кабинет\n\n"
    text += "┌ инфа про активный тариф\n"
    text += "└ Осталось дней: \n\n"
    text += f"🎁 Активная скидка: {discount}%\n\n"
    text += f"{safe}<blockquote>👥 Получай 10% скидки за каждого приглашенного друга. Подробнее по кнопке 'Реферальная программа'</blockquote>"
    
    await message.answer(
        text,
        reply_markup=account_keyboard(),
        parse_mode="HTML"
    )
