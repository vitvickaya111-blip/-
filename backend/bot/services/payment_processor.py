"""Payment processing and product access granting"""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from aiogram.types import URLInputFile

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
    # Update user
    await repo.users.update(user_id, has_paid_pdf=True)

    # Send PDF
    paid_pdf_url = settings.misc.paid_pdf_url

    if paid_pdf_url:
        try:
            pdf_file = URLInputFile(paid_pdf_url, filename="relocation_full_guide.pdf")
            await bot.send_document(
                user_id,
                pdf_file,
                caption=(
                    "📕 **ВОТ ТВОЙ ПОЛНЫЙ ГАЙД ПО РЕЛОКАЦИИ!**\n\n"
                    "Это твоя дорожная карта к свободе.\n\n"
                    "Изучай, планируй, действуй! 💜\n\n"
                    "Если возникнут вопросы — пиши мне в личку, я всегда помогу!"
                ),
                parse_mode="Markdown"
            )
        except Exception:
            # If PDF sending fails, send link
            await bot.send_message(
                user_id,
                f"📕 **ВОТ ТВОЙ ПОЛНЫЙ ГАЙД ПО РЕЛОКАЦИИ!**\n\n"
                f"📥 Скачать: {paid_pdf_url}\n\n"
                f"Изучай, планируй, действуй! 💜",
                parse_mode="Markdown"
            )
    else:
        # TODO: PDF URL not configured yet
        await bot.send_message(
            user_id,
            "📕 **ДОСТУП К ПОЛНОМУ ГАЙДУ АКТИВИРОВАН!**\n\n"
            "⚠️ PDF файл будет отправлен в ближайшее время.\n\n"
            "Спасибо за покупку! 💜",
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
        try:
            # Create invite link
            invite_link = await bot.create_chat_invite_link(
                community_chat_id,
                member_limit=1,
                name=f"User {user_id}"
            )

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
        # TODO: Community chat not configured yet
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
