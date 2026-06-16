from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "join")
async def joinb(callback: CallbackQuery):
    await callback.answer("Функция в разработке", show_alert=True)