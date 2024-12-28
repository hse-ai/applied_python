## Разработка Telegram-бота с использованием aiogram 3.x

### 1. Установка и настройка

#### Установка библиотеки

```bash
pip install aiogram
```

#### Создание бота в Telegram

1. Перейдите к боту `@BotFather` в Telegram.
2. Используйте команду `/newbot` для создания нового бота.
3. Сохраните токен вашего бота.

### 2. Основные компоненты aiogram

#### **Bot**

Класс `Bot` предоставляет доступ к Telegram API.

```python
from aiogram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")
```

#### **Dispatcher**

`Dispatcher` управляет обработчиками событий.

```python
from aiogram import Dispatcher

dp = Dispatcher()
```

#### **Handlers (Обработчики)**

Обработчики обрабатывают события, такие как команды, текстовые сообщения или нажатия кнопок.

```python
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message()
async def handle_message(message: Message):
    await message.reply(f"Вы отправили: {message.text}")
```

#### **Middleware**

Middleware позволяет выполнять действия до и после обработки события.

```python
from aiogram import BaseMiddleware
from aiogram.types import Message

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        print(f"Получено сообщение: {event.text}")
        return await handler(event, data)
```

### 3. Создание простого бота

#### Файл `bot.py`

```python
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Создаем экземпляры бота и диспетчера
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Добро пожаловать! Я ваш бот.")

# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply("Я могу ответить на команды /start и /help.")

# Основная функция запуска бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```


### 4. Обработка команд, текста и кнопок

#### Обработка текста

```python
@dp.message()
async def echo_message(message: Message):
    await message.reply(f"Вы сказали: {message.text}")
```

#### Инлайн-клавиатуры

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton(text="Кнопка 2", callback_data="btn2")],
    ]
)

@dp.message(Command("keyboard"))
async def show_keyboard(message: Message):
    await message.reply("Выберите опцию:", reply_markup=keyboard)

@dp.callback_query()
async def handle_callback(callback_query):
    if callback_query.data == "btn1":
        await callback_query.message.reply("Вы нажали Кнопка 1")
    elif callback_query.data == "btn2":
        await callback_query.message.reply("Вы нажали Кнопка 2")
```

### 5. Работа с состояниями (FSM)

**FSM** (Finite State Machine) позволяет управлять сложными сценариями.

#### Определение состояний

```python
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()
```

#### Использование состояний

```python
from aiogram.fsm.context import FSMContext

@dp.message(Command("form"))
async def start_form(message: Message, state: FSMContext):
    await message.reply("Как вас зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Сколько вам лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = message.text
    await message.reply(f"Привет, {name}! Тебе {age} лет.")
    await state.clear()
```

### 6. Расширенные возможности

#### Работа с API

```python
import aiohttp

@dp.message(Command("joke"))
async def get_joke(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.chucknorris.io/jokes/random") as response:
            joke = await response.json()
            await message.reply(joke["value"])
```

### 7. Деплой бота

#### Использование Docker

Создайте файл `Dockerfile`:

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Соберите и запустите образ:

```bash
docker build -t my_telegram_bot .
docker run -d --name my_telegram_bot my_telegram_bot
```
