import os

from dotenv import load_dotenv

# Суперподробное логирование для отладки
import logging
logging.basicConfig(level=logging.DEBUG)

aiohttp_logger = logging.getLogger("aiohttp")
aiohttp_logger.setLevel(logging.DEBUG)

# Загрузка переменных из .env файла
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CURRENCY_API_KEY = os.getenv("API_TOKEN")
CURRENCY_API_URL = "https://api.apilayer.com/exchangerates_data/latest"

if not API_TOKEN or not CURRENCY_API_KEY:
    raise NameError
