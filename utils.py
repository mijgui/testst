from aiogram.types import Message, CallbackQuery
from discounts import get_discount, get_users_count
from keyboards import main_menu_keyboard, admin_keyboard, account_reply_keyboard
from referral_system import load_referrals
from promocodes import load_promocodes
from config import ADMIN_IDS


async def is_subscribed(bot, user_id: int, channel_username: str) -> bool:
    """Проверить подписку пользователя на канал"""
    from aiogram.enums import ChatMemberStatus
    try:
        member = await bot.get_chat_member(channel_username, user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except:
        return False


async def safe_edit_or_send(callback: CallbackQuery, text: str, reply_markup=None, parse_mode: str = "HTML"):
    """
    Безопасно отредактировать сообщение или отправить новое если ошибка.
    Использует edit_text вместо удаления и отправки нового.
    """
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception:
        try:
            await callback.message.answer(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        except:
            pass
    await callback.answer()


async def safe_delete(message: Message):
    """Безопасное удаление сообщения"""
    try:
        await message.delete()
    except:
        pass


async def send_main_menu(bot, chat_id: int, user_id: int):
    """Отправить главное меню с информацией о скидке если есть"""
    discount = get_discount(user_id)
    if discount:
        text = f"🏠 Главное меню\n\n🎉 Ваша активная скидка: {discount}%"
    else:
        text = "🏠 Главное меню"
    
    await bot.send_message(
        chat_id,
        text=text,
        reply_markup=main_menu_keyboard()
    )


async def send_admin_panel(bot, chat_id: int, user_id: int):
    """Отправить администраторскую панель"""
    if user_id not in ADMIN_IDS:
        return
    
    users_count = get_users_count()
    referrals = load_referrals()
    referrers = set(referrals.values()) if referrals else set()
    promocodes = load_promocodes()
    
    text = f"📊 Статистика:\n\n"
    text += f"👥 Всего пользователей: {users_count}\n"
    text += f"🔗 Всего рефералов: {len(referrals)}\n"
    text += f"👤 Уникальных пригласивших: {len(referrers)}\n"
    text += f"🎫 Промокодов: {len(promocodes)}"
    
    await bot.send_message(chat_id, text, reply_markup=admin_keyboard())


async def edit_admin_panel(callback: CallbackQuery, user_id: int):
    """Отредактировать сообщение на админ-панель"""
    if user_id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    users_count = get_users_count()
    referrals = load_referrals()
    referrers = set(referrals.values()) if referrals else set()
    promocodes = load_promocodes()
    
    text = f"📊 Статистика:\n\n"
    text += f"👥 Всего пользователей: {users_count}\n"
    text += f"🔗 ��сего рефералов: {len(referrals)}\n"
    text += f"👤 Уникальных пригласивших: {len(referrers)}\n"
    text += f"🎫 Промокодов: {len(promocodes)}"
    
    await safe_edit_or_send(
        callback,
        text=text,
        reply_markup=admin_keyboard()
    )
