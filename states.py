from aiogram.fsm.state import State, StatesGroup


class PromoState(StatesGroup):
    """Состояние для ввода промокода в реферальной программе"""
    waiting = State()


class AdminPromoState(StatesGroup):
    """Состояние для добавления промокода админом"""
    waiting_code = State()
    waiting_discount = State()
