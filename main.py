import json
import os
from config import TOKEN, DISCOUNTS_FILE, PROMOCODES_FILE
from discounts import load_discounts
from handlers import (
    start_router,
    navigation_router,
    tariffs_router,
    referral_router,
    join_router,
    admin_router,
    account_router
)
from aiogram import Bot, Dispatcher
import asyncio

bot = Bot(TOKEN)
dp = Dispatcher()

async def main():
    # Создаём файлы, если их нет
    if not os.path.exists(DISCOUNTS_FILE):
        with open(DISCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        print("✅ Создан файл discounts.json")

    if not os.path.exists(PROMOCODES_FILE):
        with open(PROMOCODES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)   # пустой список
        print("✅ Создан файл promocodes.json")

    load_discounts()

    dp.include_router(start_router)
    dp.include_router(navigation_router)
    dp.include_router(tariffs_router)
    dp.include_router(referral_router)
    dp.include_router(join_router)
    dp.include_router(admin_router)
    dp.include_router(account_router) 

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())