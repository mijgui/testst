from aiogram.fsm.state import State, StatesGroup

class PromoState(StatesGroup):
    waiting = State()