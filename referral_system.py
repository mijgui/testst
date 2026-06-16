import json
import os

REFERRALS_FILE = "referrals.json"  # referee -> referrer

def load_referrals():
    if os.path.exists(REFERRALS_FILE):
        with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_referrals(data):
    with open(REFERRALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_referrer(referee_user_id: int):
    """Кто пригласил данного пользователя"""
    data = load_referrals()
    return data.get(str(referee_user_id))

def set_referrer(referee_user_id: int, referrer_user_id: int) -> bool:
    """Записывает, кто пригласил. Возвращает True, если запись новая."""
    data = load_referrals()
    key = str(referee_user_id)
    if key in data:
        return False
    data[key] = referrer_user_id
    save_referrals(data)
    return True