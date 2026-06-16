import json
import os
from config import PROMOCODES_FILE

def load_promocodes():
    if os.path.exists(PROMOCODES_FILE):
        with open(PROMOCODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_promocodes(promocodes):
    with open(PROMOCODES_FILE, "w", encoding="utf-8") as f:
        json.dump(promocodes, f, ensure_ascii=False, indent=2)

def add_promocode(code, discount):
    promocodes = load_promocodes()
    for item in promocodes:
        if item["code"].upper() == code.upper():
            return False  # уже существует
    promocodes.append({"code": code.upper(), "discount": discount})
    save_promocodes(promocodes)
    return True