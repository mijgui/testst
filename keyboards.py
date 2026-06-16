from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHANNEL_USERNAME


def subscribe_keyboard():
    """Клавиатура для подписки на канал"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
        ]
    )


def main_menu_keyboard():
    """Главное меню с основными разделами"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📦 Тарифы", callback_data="menu:tariffs"))
    builder.row(InlineKeyboardButton(text="🚀 Подключить", callback_data="menu:join"))
    builder.row(InlineKeyboardButton(text="🎁 Реферальная программа", callback_data="menu:referral"))
    builder.row(
        InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/mijgui"),
        InlineKeyboardButton(text="📢 Канал", url="https://t.me/vpntestttt")
    )
    return builder.as_markup()


def account_reply_keyboard():
    """Reply-клавиатура с кнопкой личного кабинета (доступна везде)"""
    buttons = [
        [KeyboardButton(text="👤 Личный кабинет")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )


def tariffs_keyboard():
    """Клавиатура выбора тарифов с кнопкой назад"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗓 1 месяц - 199 руб", callback_data="menu:tariffs:buy_1")],
            [InlineKeyboardButton(text="📆 3 месяца - 499 руб", callback_data="menu:tariffs:buy_3")],
            [InlineKeyboardButton(text="🏆 12 месяцев - 999 руб", callback_data="menu:tariffs:buy_12")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
        ]
    )


def referral_keyboard():
    """Клавиатура реферальной программы"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎫 Промокоды", callback_data="menu:referral:promocodes"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()


def promocode_request_keyboard():
    """Клавиатура для отмены ввода промокода"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu:referral:cancel_promo")]
        ]
    )


def account_keyboard():
    """Клавиатура личного кабинета"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚀 Подключить", callback_data="menu:join"))
    builder.row(InlineKeyboardButton(text="🎁 Реферальная программа", callback_data="menu:referral"))
    builder.row(
        InlineKeyboardButton(text="❓ FAQ", url="https://telegra.ph/fd-06-15-16"),
        InlineKeyboardButton(text="🫂 Поддержка", url="https://t.me/mijgui")
    )
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()


def payment_keyboard():
    """Клавиатура выбора способа оплаты"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💳 СБП", callback_data="menu:tariffs:payment:sbp"))
    builder.row(InlineKeyboardButton(text="₿ Криптовалюта", callback_data="menu:tariffs:payment:crypto"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()


def admin_keyboard():
    """Клавиатура админ-панели"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Добавить промокод", callback_data="menu:admin:add_promo"))
    builder.row(InlineKeyboardButton(text="📋 Список промокодов", callback_data="menu:admin:list_promos"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()


def admin_cancel_keyboard():
    """Клавиатура для отмены добавления промокода"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu:admin:cancel_add_promo")]]
    )


def admin_list_keyboard():
    """Клавиатура списка промокодов в админ-панели"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Добавить промокод", callback_data="menu:admin:add_promo"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()
