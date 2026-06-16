from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils import safe_edit_or_send
from discounts import get_discount
from keyboards import account_keyboard
from navigation_manager import nav_manager, MenuLevel
import html

router = Router()


@router.callback_query(F.data == "menu:account")
async def account_info(callback: CallbackQuery, state: FSMContext):
    """Показать информацию личного кабинета"""
    await state.clear()
    user_id = callback.from_user.id
    nav_manager.push_level(user_id, MenuLevel.ACCOUNT)
    
    discount = get_discount(user_id)
    safe = html.escape("")
    
    text = f"👤 Личный кабинет\n\n"
    text += "┌ инфа про активный тариф\n"
    text += "└ Осталось дней: \n\n"
    text += f"🎁 Активная скидка: {discount}%\n\n"
    text += f"{safe}<blockquote>👥 Получай 10% скидки за каждого приглашенного друга. Подробнее по кнопке 'Реферальная программа'</blockquote>"
    
    await safe_edit_or_send(
        callback,
        text=text,
        reply_markup=account_keyboard(),
        parse_mode="HTML"
    )
