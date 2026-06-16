from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils import safe_delete, send_main_menu

router = Router()

@router.callback_query(F.data == "back_menu")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_delete(callback.message)
    await send_main_menu(callback.bot, callback.message.chat.id, callback.from_user.id)

# @router.callback_query(F.data == "back_panel")
# async def back_panel(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await safe_delete(callback.message)
#     await send_main_menu(callback.bot, callback.message.chat.id, callback.from_user.id)