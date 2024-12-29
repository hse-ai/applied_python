import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import API_TOKEN
from utils import get_exchange_rate

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class CurrencyConversion(StatesGroup):
    base_currency = State()
    target_currency = State()


currency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="USD"), KeyboardButton(text="EUR"), KeyboardButton(text="RUB")],
        [KeyboardButton(text="USD to RUB"), KeyboardButton(text="EUR to RUB")],
    ],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот, который проверяет текущий курс валют. Поддерживается два режима:\n"
        "1. В сценарии /convert : введите базовую валюту, потом валюту, в которую вы хотите сконвертировать;\n"
        "2. Введите запрос в формате 'USD to RUB.'\n"
        "Популярные валюты и конвертации представлены в виде кнопок.\n",
        reply_markup=currency_keyboard,
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Привет! Я бот, который проверяет текущий курс валют. Поддерживается два режима:\n"
        "1. В сценарии /convert : введите базовую валюту, потом валюту, в которую вы хотите сконвертировать;\n"
        "2. Введите запрос в формате 'USD to RUB.'\n"
        "Популярные валюты и конвертации представлены в виде кнопок.\n"
        "/start - Начать работу\n"
        "/help - Помощь"
    )


@dp.message(Command("convert"))
async def start_conversion(message: Message, state: FSMContext):
    """Начало конверсии валют через FSM."""
    await state.set_state(CurrencyConversion.base_currency)
    await message.answer("Выберите базовую валюту:", reply_markup=currency_keyboard)


@dp.message(CurrencyConversion.base_currency)
async def select_base_currency(message: Message, state: FSMContext):
    """Выбор базовой валюты."""
    await state.update_data(base_currency=message.text)
    await state.set_state(CurrencyConversion.target_currency)
    await message.answer("Теперь выберите валюту для конвертации:", reply_markup=currency_keyboard)


@dp.message(CurrencyConversion.target_currency)
async def select_target_currency(message: Message, state: FSMContext):
    """Выбор валюты для конверсии."""
    data = await state.get_data()
    base_currency = data["base_currency"]
    target_currency = message.text

    rate = await get_exchange_rate(base_currency, target_currency)  # Асинхронный запрос
    if rate is None:
        await message.answer("Ошибка при получении курса.")
    else:
        await message.answer(f"Курс {base_currency} к {target_currency}: {rate:.5f}")

    await state.clear()


@dp.message()
async def convert_currency(message: Message):
    """Обработка текстовых запросов в формате 'USD to RUB'."""
    try:
        parts = message.text.split(" to ")
        if len(parts) != 2:
            await message.answer("Введите запрос в формате 'USD to RUB'.")
            return

        base_currency, target_currency = parts
        rate = await get_exchange_rate(base_currency, target_currency)

        if rate is None:
            await message.answer("Не удалось получить курс. Убедитесь, что валюты указаны корректно.")
            return

        await message.answer(f"Курс {base_currency} к {target_currency}: {rate:.5f}")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
