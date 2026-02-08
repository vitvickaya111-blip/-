import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.db import (
    get_pending_funnel_messages, mark_funnel_message_sent,
    get_inactive_users, mark_reactivation_sent,
)
from texts.messages import (
    FUNNEL_STEP_1, FUNNEL_STEP_2, FUNNEL_STEP_3, FUNNEL_STEP_4,
    REACTIVATION_MESSAGE,
)

logger = logging.getLogger(__name__)

FUNNEL_TEXTS = {
    1: FUNNEL_STEP_1,
    2: FUNNEL_STEP_2,
    3: FUNNEL_STEP_3,
    4: FUNNEL_STEP_4,
}


async def send_funnel_messages(bot: Bot):
    """Отправить все запланированные сообщения воронки"""
    try:
        messages = await get_pending_funnel_messages()
    except Exception as e:
        logger.error(f"Ошибка получения сообщений воронки: {e}")
        return

    for msg in messages:
        step = msg['step']
        user_id = msg['user_id']
        message_id = msg['id']
        text = FUNNEL_TEXTS.get(step)

        if not text:
            continue

        try:
            await bot.send_message(user_id, text)
            await mark_funnel_message_sent(message_id)
            logger.info(f"Воронка: отправлено сообщение шаг {step} пользователю {user_id}")
        except Exception as e:
            logger.error(f"Воронка: ошибка отправки шаг {step} пользователю {user_id}: {e}")
            # Если пользователь заблокировал бота — помечаем как отправленное
            if "Forbidden" in str(e) or "blocked" in str(e):
                await mark_funnel_message_sent(message_id)


async def send_reactivation_messages(bot: Bot):
    """Отправить реактивационные сообщения неактивным пользователям"""
    try:
        users = await get_inactive_users(days=7)
    except Exception as e:
        logger.error(f"Ошибка получения неактивных пользователей: {e}")
        return

    for user_id in users:
        try:
            await bot.send_message(user_id, REACTIVATION_MESSAGE)
            await mark_reactivation_sent(user_id)
            logger.info(f"Реактивация: отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Реактивация: ошибка отправки пользователю {user_id}: {e}")
            if "Forbidden" in str(e) or "blocked" in str(e):
                await mark_reactivation_sent(user_id)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Настроить и вернуть планировщик"""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_funnel_messages,
        'interval',
        minutes=5,
        args=[bot],
        id='funnel_sender',
        replace_existing=True,
    )
    scheduler.add_job(
        send_reactivation_messages,
        'interval',
        minutes=60,
        args=[bot],
        id='reactivation_sender',
        replace_existing=True,
    )
    return scheduler
