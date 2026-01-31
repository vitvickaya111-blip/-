import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db
from keyboards.reply import main_menu
from services.funnel_scheduler import setup_scheduler

# Импорт роутеров
from handlers import start, services, education, cases, consultation, about, funnel

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Catch-all роутер — подключается последним
fallback_router = Router()


@fallback_router.message(F.text)
async def unknown_text(message: Message):
    await message.answer(
        "Не понимаю эту команду.\n"
        "Используйте кнопки меню ниже.",
        reply_markup=main_menu()
    )


async def main():
    """Главная функция"""
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Инициализация БД
    await init_db()

    # Подключение роутеров (порядок важен!)
    dp.include_router(start.router)
    dp.include_router(funnel.router)
    dp.include_router(services.router)
    dp.include_router(education.router)
    dp.include_router(cases.router)
    dp.include_router(consultation.router)
    dp.include_router(about.router)
    dp.include_router(fallback_router)  # последний — ловит всё остальное

    # Запуск планировщика воронки
    scheduler = setup_scheduler(bot)
    scheduler.start()

    # Запуск бота
    print("Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
