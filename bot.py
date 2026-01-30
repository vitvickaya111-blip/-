import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db

# Импорт роутеров
from handlers import start, services, education, cases, consultation, about

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def main():
    """Главная функция"""
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Инициализация БД
    await init_db()

    # Подключение роутеров
    dp.include_router(start.router)
    dp.include_router(services.router)
    dp.include_router(education.router)
    dp.include_router(cases.router)
    dp.include_router(consultation.router)
    dp.include_router(about.router)

    # Запуск бота
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
