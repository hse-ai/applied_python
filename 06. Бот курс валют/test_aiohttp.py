# Проверка что работает aiohttp
import aiohttp
import asyncio
from config import API_TOKEN

async def test_aiohttp():
    url = f"https://api.telegram.org/bot{API_TOKEN}/getMe"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                print("Подключение успешно!")
                print(await response.json())
            else:
                print(f"Ошибка: {response.status}")

asyncio.run(test_aiohttp())
