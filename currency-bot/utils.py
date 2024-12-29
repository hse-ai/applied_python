import asyncio
import aiohttp
from config import CURRENCY_API_KEY, CURRENCY_API_URL


async def get_exchange_rate(base_currency: str, target_currency: str) -> float | None:
    headers = {"apikey": CURRENCY_API_KEY}
    params = {"base": base_currency.upper()}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(CURRENCY_API_URL, headers=headers, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data.get("rates", {})
                    return rates.get(target_currency.upper())
                else:
                    print(f"Ошибка API: {response.status}, {await response.text()}")
        except aiohttp.ClientError as e:
            print(f"Ошибка клиента API: {e}")
        except asyncio.TimeoutError:
            print("Ошибка: Таймаут при запросе к API")
    return None
