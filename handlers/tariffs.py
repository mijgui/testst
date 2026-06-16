from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import PRICES
from keyboards import tariffs_keyboard, payment_keyboard
from utils import safe_delete, send_main_menu
from discounts import get_discount   # пока не удаляем скидку

router = Router()

@router.callback_query(F.data == "tariffs")
async def tariffs(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
    text="📦 Тарифы\n\n",
    reply_markup=tariffs_keyboard(),
    parse_mode="Markdown")
    # await safe_delete(callback.message)
    # await callback.message.answer(text="📦 Тарифы\n\n", reply_markup=tariffs_keyboard())

@router.callback_query(F.data.startswith("buy_"))
async def buy_tariff(callback: CallbackQuery):
    user_id = callback.from_user.id
    tariff = callback.data.split("_")[1]  # '1', '3', '12'
    
    tariff_names = {
        "1": "1 месяц",
        "3": "3 месяца",
        "12": "12 месяцев"
    }
    tariff_name = tariff_names.get(tariff, tariff)
    base_price = PRICES.get(tariff, 0)
    discount = get_discount(user_id)  # получаем скидку, но пока не удаляем
    final_price = int(base_price * (100 - discount) / 100)
    
    # Формируем текст сообщения
    text = f"📋 Тариф: *{tariff_name}*\n\n"
    if discount > 0:
        text += f"🎁 Ваша скидка: {discount}%\n"
        text += f"💵 Итоговая цена: *{final_price} руб.*\n\n"
    else:
        text += f"💵 Цена: *{final_price} руб.*\n\n"
    text += "Выберите способ оплаты:"
    
    await safe_delete(callback.message)  # удаляем сообщение с тарифами
    await callback.message.answer(
        text,
        reply_markup=payment_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# ---------- Обработчики оплаты (заглушки) ----------
@router.callback_query(F.data == "pay_sbp")
async def pay_sbp(callback: CallbackQuery):
    # Здесь будет реальная логика оплаты через СБП
    await callback.answer("💳 Оплата через СБП в разработке", show_alert=True)
    # Можно вернуть в главное меню или остаться на этом же сообщении

@router.callback_query(F.data == "pay_crypto")
async def pay_crypto(callback: CallbackQuery):
    # Здесь будет реальная логика оплаты криптовалютой
    await callback.answer("₿ Оплата криптовалютой в разработке", show_alert=True)

@router.callback_query(F.data == "back_tarrifs")
async def back_tarrifs(callback: CallbackQuery):
    await tariffs(callback)