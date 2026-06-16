"""
Менеджер для управления иерархической навигацией.
Отслеживает текущий уровень меню и предоставляет методы для навигации.
"""

from typing import Optional, Dict, Callable
from enum import Enum


class MenuLevel(Enum):
    """Уровни меню в иерархии"""
    MAIN = "menu"
    ACCOUNT = "menu:account"
    ACCOUNT_REFERRAL = "menu:account:referral"
    TARIFFS = "menu:tariffs"
    TARIFF_PAYMENT = "menu:tariffs:payment"
    REFERRAL = "menu:referral"
    PROMOCODES = "menu:referral:promocodes"
    ADMIN = "menu:admin"
    ADMIN_ADD_PROMO = "menu:admin:add_promo"
    ADMIN_LIST_PROMOS = "menu:admin:list_promos"


class NavigationManager:
    """Управляет навигацией между уровнями меню"""
    
    def __init__(self):
        # Словарь соответствия callback_data → MenuLevel
        self.callback_to_level: Dict[str, MenuLevel] = {
            "menu": MenuLevel.MAIN,
            "account": MenuLevel.ACCOUNT,
            "account_referral": MenuLevel.ACCOUNT_REFERRAL,
            "tariffs": MenuLevel.TARIFFS,
            "payment": MenuLevel.TARIFF_PAYMENT,
            "reff": MenuLevel.REFERRAL,
            "promocodes": MenuLevel.PROMOCODES,
            "admin": MenuLevel.ADMIN,
            "admin_add_promo": MenuLevel.ADMIN_ADD_PROMO,
            "admin_list_promos": MenuLevel.ADMIN_LIST_PROMOS,
        }
        
        # История навигации пользователей: user_id → list of MenuLevels
        self.history: Dict[int, list] = {}
    
    def get_level_from_callback(self, callback_data: str) -> Optional[MenuLevel]:
        """Получить уровень меню из callback_data"""
        return self.callback_to_level.get(callback_data)
    
    def push_level(self, user_id: int, level: MenuLevel):
        """Добавить уровень в историю"""
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append(level)
    
    def pop_level(self, user_id: int) -> Optional[MenuLevel]:
        """Вернуться на предыдущий уровень"""
        if user_id in self.history and len(self.history[user_id]) > 1:
            self.history[user_id].pop()
            return self.history[user_id][-1]
        return MenuLevel.MAIN
    
    def get_current_level(self, user_id: int) -> MenuLevel:
        """Получить текущий уровень меню"""
        if user_id not in self.history or not self.history[user_id]:
            return MenuLevel.MAIN
        return self.history[user_id][-1]
    
    def reset_history(self, user_id: int):
        """Очистить историю навигации (вернуться в главное меню)"""
        if user_id in self.history:
            self.history[user_id] = [MenuLevel.MAIN]
    
    def get_parent_level(self, level: MenuLevel) -> MenuLevel:
        """Получить родительский уровень для текущего"""
        parent_map = {
            MenuLevel.MAIN: MenuLevel.MAIN,
            MenuLevel.ACCOUNT: MenuLevel.MAIN,
            MenuLevel.ACCOUNT_REFERRAL: MenuLevel.ACCOUNT,
            MenuLevel.TARIFFS: MenuLevel.MAIN,
            MenuLevel.TARIFF_PAYMENT: MenuLevel.TARIFFS,
            MenuLevel.REFERRAL: MenuLevel.MAIN,
            MenuLevel.PROMOCODES: MenuLevel.REFERRAL,
            MenuLevel.ADMIN: MenuLevel.MAIN,
            MenuLevel.ADMIN_ADD_PROMO: MenuLevel.ADMIN,
            MenuLevel.ADMIN_LIST_PROMOS: MenuLevel.ADMIN,
        }
        return parent_map.get(level, MenuLevel.MAIN)


# Глобальный экземпляр менеджера
nav_manager = NavigationManager()
