import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import setup_handlers
from middlewares import LoggingMiddleware

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем middleware и обработчики
dp.message.middleware(LoggingMiddleware())
setup_handlers(dp)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
