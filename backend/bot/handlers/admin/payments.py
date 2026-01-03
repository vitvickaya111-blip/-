"""Admin payment approval handlers"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.admin import IsAdmin
from infrastructure.database.requests import RequestsRepo
from services.payment_processor import grant_product_access
from utils.constants import PRODUCT_NAMES

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("approve"))
async def approve_payment_command(message: Message, repo: RequestsRepo, config):
    """
    Approve pending payment: /approve USER_ID

    Example: /approve 123456789
    """
    try:
        # Parse user_id from command
        parts = message.text.split()
        if len(parts) != 2:
            await message.answer(
                "❌ Неверный формат команды.\n\n"
                "Используй: `/approve USER_ID`\n\n"
                "Пример: `/approve 123456789`",
                parse_mode="Markdown"
            )
            return

        user_id = int(parts[1])

        # Find pending payment for this user
        payment = await repo.payments.get_pending_by_user(user_id)

        if not payment:
            await message.answer(
                f"❌ Нет ожидающих платежей для пользователя {user_id}"
            )
            return

        # Approve payment
        await repo.payments.approve_payment(payment.id)

        # Grant product access
        await grant_product_access(
            user_id,
            payment.product_type,
            repo,
            message.bot,
            config
        )

        # Notify user about approval
        product_name = PRODUCT_NAMES.get(payment.product_type, "продукт")

        try:
            await message.bot.send_message(
                user_id,
                f"✅ **ПЛАТЕЖ ПОДТВЕРЖДЕН!**\n\n"
                f"Твоя покупка: {product_name}\n"
                f"Сумма: ${payment.final_amount_usd}\n\n"
                f"Доступ активирован! Проверь сообщения выше 👆\n\n"
                f"Спасибо за покупку! 💜",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ Не удалось уведомить пользователя {user_id}: {e}")

        # Notify admin about success
        await message.answer(
            f"✅ **ПЛАТЕЖ ПОДТВЕРЖДЕН**\n\n"
            f"Пользователь: {user_id}\n"
            f"Продукт: {product_name}\n"
            f"Сумма: ${payment.final_amount_usd}\n\n"
            f"Доступ выдан!",
            parse_mode="Markdown"
        )

    except ValueError:
        await message.answer(
            "❌ USER_ID должен быть числом.\n\n"
            "Пример: `/approve 123456789`",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка при подтверждении платежа:\n{str(e)}"
        )


@router.message(Command("reject"))
async def reject_payment_command(message: Message, repo: RequestsRepo):
    """
    Reject pending payment: /reject USER_ID

    Example: /reject 123456789
    """
    try:
        # Parse user_id from command
        parts = message.text.split()
        if len(parts) != 2:
            await message.answer(
                "❌ Неверный формат команды.\n\n"
                "Используй: `/reject USER_ID`\n\n"
                "Пример: `/reject 123456789`",
                parse_mode="Markdown"
            )
            return

        user_id = int(parts[1])

        # Find pending payment for this user
        payment = await repo.payments.get_pending_by_user(user_id)

        if not payment:
            await message.answer(
                f"❌ Нет ожидающих платежей для пользователя {user_id}"
            )
            return

        # Reject payment
        await repo.payments.reject_payment(payment.id)

        # Notify user about rejection
        product_name = PRODUCT_NAMES.get(payment.product_type, "продукт")

        try:
            await message.bot.send_message(
                user_id,
                f"❌ **ПЛАТЕЖ НЕ ПОДТВЕРЖДЕН**\n\n"
                f"К сожалению, платеж за \"{product_name}\" не прошел проверку.\n\n"
                f"Возможные причины:\n"
                f"• Неверная сумма\n"
                f"• Платеж не найден\n"
                f"• Технические проблемы\n\n"
                f"💬 Пожалуйста, свяжись со мной для уточнения деталей.",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ Не удалось уведомить пользователя {user_id}: {e}")

        # Notify admin about rejection
        await message.answer(
            f"❌ **ПЛАТЕЖ ОТКЛОНЕН**\n\n"
            f"Пользователь: {user_id}\n"
            f"Продукт: {product_name}\n"
            f"Сумма: ${payment.final_amount_usd}\n\n"
            f"Пользователь уведомлен.",
            parse_mode="Markdown"
        )

    except ValueError:
        await message.answer(
            "❌ USER_ID должен быть числом.\n\n"
            "Пример: `/reject 123456789`",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка при отклонении платежа:\n{str(e)}"
        )


@router.message(Command("payments"))
async def list_pending_payments(message: Message, repo: RequestsRepo):
    """
    List all pending payments
    """
    try:
        # Get all pending payments
        payments = await repo.payments.get_all_pending()

        if not payments:
            await message.answer("✅ Нет ожидающих платежей")
            return

        # Build list
        text = f"📋 **ОЖИДАЮЩИЕ ПЛАТЕЖИ** ({len(payments)})\n\n"

        for payment in payments:
            product_name = PRODUCT_NAMES.get(payment.product_type, "неизвестно")

            text += (
                f"👤 User ID: `{payment.user_id}`\n"
                f"🛍️ Продукт: {product_name}\n"
                f"💰 Сумма: ${payment.final_amount_usd}"
            )

            if payment.promo_code:
                text += f" (промокод: {payment.promo_code})"

            text += (
                f"\n📅 Дата: {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"✅ `/approve {payment.user_id}`\n"
                f"❌ `/reject {payment.user_id}`\n\n"
            )

        await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении списка платежей:\n{str(e)}")
