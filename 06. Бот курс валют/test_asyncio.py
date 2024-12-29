# Проверка что работает aiogram
import asyncio
from aiogram import Bot
from config import API_TOKEN


async def test_connection():
    bot = Bot(token=API_TOKEN, timeout=30)
    try:
        me = await bot.get_me()
        print(f"Бот подключен: {me.first_name}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        await bot.session.close()

asyncio.run(test_connection())
