"""Payment processing and product access granting"""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from aiogram.types import FSInputFile

from infrastructure.database.requests import RequestsRepo
from utils.constants import (
    PRODUCT_PAID_PDF, PRODUCT_COMMUNITY, PRODUCT_CONSULTATION_300,
    PRICES, PROMO_CODES
)


def calculate_price(product_type: str, promo_code: Optional[str] = None) -> tuple[Decimal, int]:
    """
    Calculate final price with promo code discount.

    Returns:
        tuple: (final_price, discount_percent)
    """
    base_price = Decimal(str(PRICES[product_type]))
    discount_percent = 0

    if promo_code and promo_code.upper() in PROMO_CODES:
        discount_percent = PROMO_CODES[promo_code.upper()]["discount"]
        discount_amount = base_price * Decimal(discount_percent) / Decimal(100)
        final_price = base_price - discount_amount
    else:
        final_price = base_price

    return final_price, discount_percent


async def grant_product_access(
    user_id: int,
    product_type: str,
    repo: RequestsRepo,
    bot: Bot,
    settings
) -> None:
    """
    Grant access to product after payment approval.

    Args:
        user_id: Telegram user ID
        product_type: Type of product (paid_pdf, community, consultation_300)
        repo: Database repository
        bot: Telegram bot instance
        settings: App settings
    """
    if product_type == PRODUCT_PAID_PDF:
        await grant_paid_pdf_access(user_id, repo, bot, settings)
    elif product_type == PRODUCT_COMMUNITY:
        await grant_community_access(user_id, repo, bot, settings)
    elif product_type == PRODUCT_CONSULTATION_300:
        await grant_consultation_300_access(user_id, repo, bot)


async def grant_paid_pdf_access(user_id: int, repo: RequestsRepo, bot: Bot, settings) -> None:
    """Grant access to paid PDF guide"""
    import os

    # Update user
    await repo.users.update(user_id, has_paid_pdf=True)

    # Send PDF from local file
    # Bot runs from /app/bot/, PDF is in /app/data/
    pdf_path = os.path.join(os.path.dirname(os.getcwd()), "data", "relocation_guide.pdf")

    try:
        pdf_file = FSInputFile(pdf_path, filename="ot_mechty_do_posadochnogo.pdf")
        await bot.send_document(
            user_id,
            pdf_file,
            caption=(
                "📖 **ВОТ ТВОЙ ГАЙД \"ОТ МЕЧТЫ ДО ПОСАДОЧНОГО\"!**\n\n"
                "30 страниц конкретики для твоей релокации! ✈️"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        # If PDF sending fails, notify user
        print(f"❌ Ошибка отправки PDF пользователю {user_id}: {e}")
        await bot.send_message(
            user_id,
            "📖 **ВОТ ТВОЙ ГАЙД \"ОТ МЕЧТЫ ДО ПОСАДОЧНОГО\"!**\n\n"
            "⚠️ Файл будет отправлен в ближайшее время.\n\n"
            "30 страниц конкретики для твоей релокации! ✈️",
            parse_mode="Markdown"
        )

    # Send bonuses message
    await bot.send_message(
        user_id,
        "🎁 **ТВОИ БОНУСЫ К ГАЙДУ:**\n\n"
        "**1️⃣ Промокод GUIDE10**\n"
        "→ Скидка 10% на расширенную консультацию\n"
        "→ \\$270 вместо \\$300!\n\n"
        "**2️⃣ Закрытый канал**\n"
        "→ @ambasadorsvobody_premium\n"
        "→ Обновления, кейсы, лайфхаки\n\n"
        "**3️⃣ Google-таблица для планирования**\n"
        "→ Будет в следующем сообщении!\n\n"
        "**4️⃣ Бесплатные обновления**\n"
        "→ Все новые версии гайда — бесплатно!\n\n"
        "**Изучай, планируй, действуй!** 💜\n\n"
        "Вопросы? Пиши мне прямо сюда! 💬",
        parse_mode="Markdown"
    )


async def grant_community_access(user_id: int, repo: RequestsRepo, bot: Bot, settings) -> None:
    """Grant access to closed community"""
    # Update user - 30 days subscription
    paid_until = datetime.utcnow() + timedelta(days=30)
    await repo.users.update(
        user_id,
        has_community_access=True,
        community_paid_until=paid_until
    )

    # Send invite link
    community_chat_id = settings.misc.community_chat_id

    if community_chat_id:
        print(f"🔍 Attempting to create invite link for community chat: {community_chat_id}")
        try:
            # Create invite link
            invite_link = await bot.create_chat_invite_link(
                community_chat_id,
                member_limit=1,
                name=f"User {user_id}"
            )

            print(f"✅ Invite link created successfully: {invite_link.invite_link}")

            await bot.send_message(
                user_id,
                f"👭 **ДОБРО ПОЖАЛОВАТЬ В СООБЩЕСТВО!**\n\n"
                f"Твоя подписка активна до {paid_until.strftime('%d.%m.%Y')}\n\n"
                f"📲 Вступай в закрытый чат:\n{invite_link.invite_link}\n\n"
                f"Там тебя ждут:\n"
                f"✨ Поддержка 24/7\n"
                f"📅 Еженедельные созвоны\n"
                f"🎓 Мастер-классы от экспертов\n"
                f"👩‍💼 Нетворкинг с единомышленницами\n\n"
                f"До встречи в чате! 💜",
                parse_mode="Markdown"
            )
        except Exception as e:
            # Log detailed error
            print(f"❌ Failed to create invite link for community: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Chat ID: {community_chat_id}")

            # If invite link fails, send manual instructions
            await bot.send_message(
                user_id,
                f"👭 **ДОСТУП К СООБЩЕСТВУ АКТИВИРОВАН!**\n\n"
                f"Подписка активна до {paid_until.strftime('%d.%m.%Y')}\n\n"
                f"⚠️ Ссылка на чат будет отправлена в ближайшее время.\n\n"
                f"Спасибо за покупку! 💜",
                parse_mode="Markdown"
            )
    else:
        # Community chat not configured
        print(f"⚠️ Community chat ID not configured! Cannot create invite link.")
        await bot.send_message(
            user_id,
            f"👭 **ДОСТУП К СООБЩЕСТВУ АКТИВИРОВАН!**\n\n"
            f"Подписка активна до {paid_until.strftime('%d.%m.%Y')}\n\n"
            f"⚠️ Ссылка на закрытый чат будет отправлена в ближайшее время.\n\n"
            f"Спасибо за покупку! 💜",
            parse_mode="Markdown"
        )


async def grant_consultation_300_access(user_id: int, repo: RequestsRepo, bot: Bot) -> None:
    """Grant access to extended consultation"""
    # Update user
    await repo.users.update(user_id, has_paid_consultation_300=True)

    # Send instructions
    await bot.send_message(
        user_id,
        "💎 **РАСШИРЕННАЯ КОНСУЛЬТАЦИЯ ОПЛАЧЕНА!**\n\n"
        "Спасибо за доверие! ❤️\n\n"
        "**Что дальше:**\n"
        "1️⃣ Я свяжусь с тобой в течение 24 часов\n"
        "2️⃣ Согласуем удобное время для созвона (60 минут)\n"
        "3️⃣ Проведем стратегическую сессию по твоей релокации\n"
        "4️⃣ Ты получишь персональный план на 6-12 месяцев\n"
        "5️⃣ Месяц поддержки в личных сообщениях\n\n"
        "Подготовься:\n"
        "📝 Опиши свою текущую ситуацию\n"
        "🎯 Сформулируй главные цели\n"
        "💰 Посчитай примерный бюджет\n\n"
        "До скорой встречи! 💜",
        parse_mode="Markdown"
    )
