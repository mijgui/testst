import json
import os
from config import DISCOUNTS_FILE

_user_discounts = None  # внутреннее хранилище

def _load_discounts():
    global _user_discounts
    if os.path.exists(DISCOUNTS_FILE):
        with open(DISCOUNTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            _user_discounts = {int(k): v for k, v in data.items()}
    else:
        _user_discounts = {}

def _save_discounts():
    if not os.path.exists(DISCOUNTS_FILE):
        raise FileNotFoundError(f"Файл {DISCOUNTS_FILE} не существует.")
    with open(DISCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(_user_discounts, f, ensure_ascii=False, indent=2)

def get_discount(user_id: int) -> int:
    """Вернуть скидку пользователя (0 если нет)"""
    if _user_discounts is None:
        _load_discounts()
    return _user_discounts.get(user_id, 0)

def add_discount(user_id: int, discount: int):
    if _user_discounts is None:
        _load_discounts()
    _user_discounts[user_id] = discount
    _save_discounts()

def remove_discount(user_id: int):
    if _user_discounts is None:
        _load_discounts()
    if user_id in _user_discounts:
        del _user_discounts[user_id]
        _save_discounts()

def increase_discount(user_id: int, increment: int, max_discount: int = 50) -> int:
    current = get_discount(user_id)
    new_discount = min(current + increment, max_discount)
    if new_discount != current:
        _user_discounts[user_id] = new_discount
        _save_discounts()
    return new_discount

def get_users_count():
    if _user_discounts is None:
        _load_discounts()
    return len(_user_discounts)

def load_discounts():
    """Публичная функция для принудительной загрузки скидок (для main.py)"""
    _load_discounts()

# При импорте модуля уже загружаем данные
_load_discounts()