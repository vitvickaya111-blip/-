import logging
from datetime import datetime, timedelta

from aiogram import Bot
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.models import User
from keyboards.inline import get_day0_keyboard, get_day2_keyboard, get_auto_funnel_day7_keyboard

logger = logging.getLogger(__name__)

# Auto-funnel texts from instructions
DAY_0_TEXT_QUIZ = """🙏 Спасибо, что прошла тест!

Твой результат и подарок ждут выше ⬆️

А теперь давай знакомиться ближе!

Я Настя. Год назад я сидела в квартире
в России и думала: "Неужели это всё?"

Токсичные отношения, работа в системе (ФСИН),
ощущение тупика...

Но я решилась. И сегодня:
🌴 Живу в Бразилии
☀️ Просыпаюсь от солнца
💰 Зарабатываю удалённо
❤️ Помогаю таким же, как ты

И я знаю, что ты тоже можешь!

Подписывайся на канал — там делюсь:
✅ Реальными историями
✅ Лайфхаками по визам
✅ Честными обзорами стран
✅ Поддержкой


До скорого! ✨
Настя"""

DAY_0_TEXT = """🙏 Спасибо, что скачала мой гайд!

Надеюсь, он будет тебе полезен.

Если будут вопросы — пиши, я на связи.

А ещё обязательно подпишись на мой канал "Женщины в движении" — там я делюсь обновлениями, отвечаю на вопросы подписчиц и рассказываю реальные истории без прикрас:

До скорого! ✨
Настя"""

DAY_2_TEXT = """Привет! 👋

Хочу рассказать, как оказалась во Вьетнаме.

Прилетела в Россию из Бразилии
с грудным ребёнком. $1000 в кармане.


В России — абьюз. Мамы нет (умерла в 2012).

Поняла: если останусь — сломаюсь.

Позвонила подруге:
"Одолжи. Улечу во Вьетнам.
Там дешевле всего. Выживу."

Она дала.

Улетела с $1000 и грудным ребёнком
в страну, где не знала языка,
не было связей, не было плана.

Было одно: ЖЕЛАНИЕ ВЫЖИТЬ.

И знаешь что?

Не просто выжила.
Построила жизнь.

Если тебе кажется "не получится" —
вспомни мою историю.

Я смогла с $1000 и грудным ребёнком.
Значит, сможешь и ты.

❤️ Настя

P.S. Если хочешь узнать КАК именно —
жду в канале или на консультации."""

DAY_5_TEXT = """☀️ Привет!

Вопрос тебе:

Что держит тебя на месте СЕЙЧАС?

💰 Деньги?
😰 Страх?
💔 Отношения?
👶 Дети?

Напиши мне — я читаю все сообщения.

Помогу найти выход.

Потому что выход ВСЕГДА есть.

Даже когда кажется, что нет.

Жду 💬

Настя ❤️"""

DAY_7_TEXT = """💫 Прошла неделя с нашего знакомства

Ты прошла тест и скачала гайд.
Надеюсь, было полезно.

Но я понимаю: общая информация — одно.
ТВОЯ конкретная ситуация — другое.

Поэтому предложение:

💬 КОНСУЛЬТАЦИЯ 30 МИНУТ — 500₽

Что будет:
✓ Разберём ТВОЮ ситуацию (деньги, дети, документы)
✓ Подберём страну под твой бюджет
✓ Составим план первых шагов
✓ Отвечу на ВСЕ вопросы

Это НЕ впаривание курсов.
Реальная помощь от женщины,
которая прошла через это.

После консультации получишь:
• Чёткий план действий
• Список ресурсов
• Мою поддержку

Хочешь?

Если "Нет" — больше не буду предлагать.
Но рада видеть в канале ❤️

С уважением,
Настя"""


async def send_day_0_message(bot: Bot, user_id: int):
    """Send Day 0 message (immediately after PDF download)"""
    try:
        await bot.send_message(user_id, DAY_0_TEXT, reply_markup=get_day0_keyboard())
        logger.info(f"Sent Day 0 message to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Day 0 message to user {user_id}: {e}")
        return False


async def send_day_0_message_quiz(bot: Bot, user_id: int):
    """Send Day 0 message after quiz completion"""
    try:
        await bot.send_message(user_id, DAY_0_TEXT_QUIZ)
        logger.info(f"Sent Day 0 quiz message to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Day 0 quiz message to user {user_id}: {e}")
        return False


async def send_day_2_message(bot: Bot, user_id: int):
    """Send Day 2 message"""
    try:
        await bot.send_message(user_id, DAY_2_TEXT, reply_markup=get_day2_keyboard())
        logger.info(f"Sent Day 2 message to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Day 2 message to user {user_id}: {e}")
        return False


async def send_day_5_message(bot: Bot, user_id: int):
    """Send Day 5 message"""
    try:
        await bot.send_message(user_id, DAY_5_TEXT)
        logger.info(f"Sent Day 5 message to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Day 5 message to user {user_id}: {e}")
        return False


async def send_day_7_message(bot: Bot, user_id: int):
    """Send Day 7 message (consultation offer)"""
    try:
        await bot.send_message(user_id, DAY_7_TEXT, reply_markup=get_auto_funnel_day7_keyboard())
        logger.info(f"Sent Day 7 message to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Day 7 message to user {user_id}: {e}")
        return False


async def process_auto_funnel(bot: Bot, sessionmaker: async_sessionmaker):
    """
    Process auto-funnel for all users.
    Should be called periodically (e.g., every hour).
    """
    logger.info("Starting auto-funnel processing")

    async with sessionmaker() as session:
        now = datetime.utcnow()

        # Day 0: Send immediately after PDF download (handled in handler)
        # Here we just mark it

        # Day 2: 48 hours after PDF download
        day2_cutoff = now - timedelta(hours=48)
        day2_users_stmt = select(User).where(
            User.downloaded_pdf == True,
            User.autoresponder_day == 0,
            User.created_at <= day2_cutoff
        )
        result = await session.execute(day2_users_stmt)
        day2_users = result.scalars().all()

        for user in day2_users:
            if await send_day_2_message(bot, user.id):
                await session.execute(
                    update(User).where(User.id == user.id).values(autoresponder_day=2)
                )

        # Day 5: 5 days after PDF download
        day5_cutoff = now - timedelta(days=5)
        day5_users_stmt = select(User).where(
            User.downloaded_pdf == True,
            User.autoresponder_day == 2,
            User.created_at <= day5_cutoff
        )
        result = await session.execute(day5_users_stmt)
        day5_users = result.scalars().all()

        for user in day5_users:
            if await send_day_5_message(bot, user.id):
                await session.execute(
                    update(User).where(User.id == user.id).values(autoresponder_day=5)
                )

        # Day 7: 7 days after PDF download (only if not declined)
        day7_cutoff = now - timedelta(days=7)
        day7_users_stmt = select(User).where(
            User.downloaded_pdf == True,
            User.autoresponder_day == 5,
            User.created_at <= day7_cutoff,
            User.consultation_declined == False,
            User.consultation_paid == False
        )
        result = await session.execute(day7_users_stmt)
        day7_users = result.scalars().all()

        for user in day7_users:
            if await send_day_7_message(bot, user.id):
                await session.execute(
                    update(User).where(User.id == user.id).values(autoresponder_day=7)
                )

        await session.commit()

    logger.info("Auto-funnel processing completed")
