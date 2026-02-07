import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Message, CallbackQuery, TelegramObject

from config import BOT_TOKEN
from database.db import init_db

from handlers import start, calculator, services, education, cases, consultation, about


class DebugMiddleware(BaseMiddleware):
    """Middleware для отладки - логирует все события"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger = logging.getLogger(__name__)
        state = data.get("state")
        current_state = await state.get_state() if state else None

        if isinstance(event, Message):
            logger.info(f"[MW] Message: '{event.text}', State: {current_state}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"[MW] Callback: '{event.data}', State: {current_state}")

        return await handler(event, data)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Установка команд бота"""
    commands = [
        BotCommand(command="start", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def on_startup(bot: Bot):
    """Действия при запуске"""
    logger.info("Бот запускается...")

    await init_db()
    logger.info("База данных инициализирована")

    await set_commands(bot)
    logger.info("Команды установлены")

    from config import ADMIN_ID
    try:
        await bot.send_message(
            ADMIN_ID,
            "🚀 БОТ ЗАПУЩЕН!\n\nВсе системы работают.\nГотов рассказывать о моих услугах! 💪"
        )
        logger.info("Уведомление админу отправлено")
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")

    logger.info("Бот успешно запущен!")


async def on_shutdown(bot: Bot):
    """Действия при остановке"""
    logger.info("Бот останавливается...")
    from config import ADMIN_ID
    try:
        await bot.send_message(ADMIN_ID, "🛑 БОТ ОСТАНОВЛЕН")
    except Exception:
        pass
    logger.info("Бот остановлен")


async def main():
    """Главная функция"""
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Debug middleware
    dp.message.middleware(DebugMiddleware())
    dp.callback_query.middleware(DebugMiddleware())

    # Порядок важен! FSM роутеры должны быть в правильном порядке
    dp.include_router(start.router)
    dp.include_router(calculator.router)
    dp.include_router(services.router)      # FSM brief
    dp.include_router(consultation.router)  # FSM consultation
    dp.include_router(education.router)
    dp.include_router(cases.router)
    dp.include_router(about.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
