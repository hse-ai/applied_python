from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Form
import aiohttp

router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Добро пожаловать! Я ваш бот.\nВведите /help для списка команд.")

# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/form - Пример диалога\n"
        "/keyboard - Пример кнопок\n"
        "/joke - Получить случайную шутку"
    )

# Обработчик команды /keyboard с инлайн-кнопками
@router.message(Command("keyboard"))
async def show_keyboard(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Кнопка 1", callback_data="btn1")],
            [InlineKeyboardButton(text="Кнопка 2", callback_data="btn2")],
        ]
    )
    await message.reply("Выберите опцию:", reply_markup=keyboard)

@router.callback_query()
async def handle_callback(callback_query):
    if callback_query.data == "btn1":
        await callback_query.message.reply("Вы нажали Кнопка 1")
    elif callback_query.data == "btn2":
        await callback_query.message.reply("Вы нажали Кнопка 2")

# FSM: диалог с пользователем
@router.message(Command("form"))
async def start_form(message: Message, state: FSMContext):
    await message.reply("Как вас зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Сколько вам лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = message.text
    await message.reply(f"Привет, {name}! Тебе {age} лет.")
    await state.clear()

# Получение шутки из API
@router.message(Command("joke"))
async def get_joke(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.chucknorris.io/jokes/random") as response:
            joke = await response.json()
            await message.reply(joke["value"])

# Функция для подключения обработчиков
def setup_handlers(dp):
    dp.include_router(router)
