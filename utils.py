from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from discounts import get_discount
from keyboards import main_menu_keyboard, admin_keyboard  # абсолютный импорт
from discounts import get_users_count
from referral_system import load_referrals
from promocodes import load_promocodes, add_promocode
from config import ADMIN_IDS

router = Router()

async def is_subscribed(bot, user_id: int, channel_username: str) -> bool:
    from aiogram.enums import ChatMemberStatus
    try:
        member = await bot.get_chat_member(channel_username, user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except:
        return False

async def safe_delete(message: Message):
    try:
        await message.delete()
    except:
        pass

async def send_main_menu(bot, chat_id: int, user_id: int):
    discount = get_discount(user_id)
    if discount:
        text = f"🏠 Главное меню\n\n🎉 Ваша активная скидка: {discount}%"
    else:
        text = "🏠 Главное меню"
    await bot.send_message(chat_id, text=text, reply_markup=main_menu_keyboard())

async def send_admin_panel(bot, chat_id: int, user_id: int):
    @router.message(Command("adminp"))
    async def admin_panel(message: Message):
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("⛔ Доступ запрещён.")
            return
        # Генерируем статистику
        users_count = get_users_count()
        referrals = load_referrals()
        referrers = set(referrals.values()) if referrals else set()
        promocodes = load_promocodes()
        text = f"📊 Статистика:\n\n"
        text += f"👥 Всего пользователей: {users_count}\n"
        text += f"🔗 Всего рефералов: {len(referrals)}\n"
        text += f"👤 Уникальных пригласивших: {len(referrers)}\n"
        text += f"🎫 Промокодов: {len(promocodes)}"
        await message.answer(text, reply_markup=admin_keyboard())