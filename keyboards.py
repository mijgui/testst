from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHANNEL_USERNAME
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
        ]
    )

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📦 Тарифы", callback_data="tariffs"))
    builder.row(InlineKeyboardButton(text="👤 Личный кабинет", callback_data="account"))
    builder.row(InlineKeyboardButton(text="🚀 Подключить", callback_data="join"))
    builder.row(InlineKeyboardButton(text="🎁 Реферальная программа", callback_data="reff"))
    builder.row(
        InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/mijgui"),
        InlineKeyboardButton(text="📢 Канал", url="https://t.me/vpntestttt")
    )
    return builder.as_markup()

def tariffs_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗓 1 месяц - 199 руб", callback_data="buy_1")],
            [InlineKeyboardButton(text="📆 3 месяца - 499 руб", callback_data="buy_3")],
            [InlineKeyboardButton(text="🏆 12 месяцев - 999 руб", callback_data="buy_12")],
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_menu")]
        ]
    )

def referral_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎫 Промокоды", callback_data="promocodes"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_menu"))
    return builder.as_markup()

def promocode_request_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_promo")]
        ]
    )

def account_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚀 Подключить", callback_data="join"))
    builder.row(InlineKeyboardButton(text="🎁 Реферальная программа", callback_data="reff"))
    builder.row(
        InlineKeyboardButton(text="❓ FAQ", url="https://telegra.ph/fd-06-15-16"),
        InlineKeyboardButton(text="🫂 Поддержка", url="https://t.me/mijgui")
        )
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_menu"))
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Добавить промокод", callback_data="admin_add_promo"))
    builder.row(InlineKeyboardButton(text="📋 Список промокодов", callback_data="admin_list_promos"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_menu"))
    return builder.as_markup()

def list_promo_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Добавить промокод", callback_data="admin_add_promo"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в панель", callback_data="obr_panel"))
    return builder.as_markup()

def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💳 СБП", callback_data="pay_sbp"))
    builder.row(InlineKeyboardButton(text="₿ Криптовалюта", callback_data="pay_crypto"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в тарифы", callback_data="back_tarrifs"))
    return builder.as_markup()

def main_reply_keyboard():
    """Клавиатура, которая будет отображаться над системной клавиатурой"""
    buttons = [
        [KeyboardButton(text="👤 Личный кабинет")],
        [KeyboardButton(text="📦 Тарифы")],
        # Можно добавить другие кнопки, но не перегружайте
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,  # кнопки подстраиваются под ширину экрана
        one_time_keyboard=False,  # остаются после нажатия
        input_field_placeholder="Выберите действие..."
    )