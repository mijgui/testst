from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import safe_delete
from discounts import get_discount
from keyboards import account_keyboard
from aiogram.types import Message
import html

router = Router()   

@router.callback_query(F.data == "account")
async def account_info(callback: CallbackQuery):
    user_id = callback.from_user.id
    discount = get_discount(user_id)  # получаем текущую скидку
    safe = html.escape("")

    text = f"👤 Личный кабинет\n\n"
    text += "┌ инфа про активный тариф\n"
    text += "└ Осталось дней: \n\n"
    text += f"🎁 Активная скидка: {discount}%\n\n"
    # text += f"📅 Дата регистрации: (если храните где-то)\n\n"
    text += f"{safe}<blockquote>👥 Получай 10% скидки за каждого приглашенного друга. Подробнее по кнопке 'Реферальная программа'</blockquote>\n"
    
    # await safe_delete(callback.message)  # удаляем предыдущее сообщение (меню)
    # await callback.message.answer(
    #     text,
    #     reply_markup=account_keyboard(),
    #     parse_mode="HTML"
    # )
    await callback.message.edit_text(
    text=text,
    reply_markup=account_keyboard(),
    parse_mode="HTML")
    await callback.answer()