"""Admin payment approval handlers"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from filters.admin import AdminFilter
from infrastructure.database.requests import RequestsRepo
from keyboards.inline import CB_ADMIN_APPROVE_PAYMENT, CB_ADMIN_REJECT_PAYMENT
from services.payment_processor import grant_product_access
from utils.constants import PRODUCT_NAMES

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command("getchatid"))
async def get_chat_id_command(message: Message):
    """Get chat ID - use this command in the chat to get its ID"""
    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_title = message.chat.title if message.chat.title else "Private chat"

    await message.answer(
        f"💬 **Информация о чате:**\n\n"
        f"Название: {chat_title}\n"
        f"Тип: `{chat_type}`\n\n"
        f"**Chat ID:**\n`{chat_id}`\n\n"
        f"💡 Скопируй chat_id и добавь в настройки:\n"
        f"`MISC__COMMUNITY_CHAT_ID={chat_id}`",
        parse_mode="Markdown"
    )


@router.message(Command("getfileid"), F.document)
async def get_file_id_command(message: Message):
    """Get file_id of uploaded document - send document with /getfileid"""
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_size = message.document.file_size / 1024 / 1024  # Convert to MB

    await message.answer(
        f"📄 **Информация о файле:**\n\n"
        f"Название: `{file_name}`\n"
        f"Размер: {file_size:.2f} MB\n\n"
        f"**File ID:**\n`{file_id}`\n\n"
        f"💡 Скопируй file_id и отправь мне, я добавлю его в настройки бота!",
        parse_mode="Markdown"
    )


@router.message(F.document)
async def handle_document_upload(message: Message):
    """Handle any document upload from admin"""
    file_id = message.document.file_id
    file_name = message.document.file_name

    await message.answer(
        f"📄 Получен файл: `{file_name}`\n\n"
        f"**File ID:**\n`{file_id}`\n\n"
        f"💡 Используй команду `/getfileid` вместе с документом для детальной информации",
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith(CB_ADMIN_APPROVE_PAYMENT))
async def approve_payment_button(callback: CallbackQuery, repo: RequestsRepo, settings):
    """
    Approve pending payment via button click

    Callback data format: admin_approve_payment:PAYMENT_ID
    """
    try:
        # Parse payment_id from callback data
        payment_id = int(callback.data.split(":")[1])

        # Get payment
        payment = await repo.payments.get_payment_by_id(payment_id)

        if not payment:
            await callback.answer("❌ Платеж не найден", show_alert=True)
            return

        if payment.status != "pending":
            await callback.answer(f"❌ Платеж уже обработан (статус: {payment.status})", show_alert=True)
            return

        # Approve payment
        await repo.payments.approve_payment(payment.id)

        # Grant product access
        await grant_product_access(
            payment.user_id,
            payment.product_type,
            repo,
            callback.bot,
            settings
        )

        # Notify user about approval
        product_name = PRODUCT_NAMES.get(payment.product_type, "продукт")

        try:
            await callback.bot.send_message(
                payment.user_id,
                f"✅ **ПЛАТЕЖ ПОДТВЕРЖДЕН!**\n\n"
                f"Твоя покупка: {product_name}\n"
                f"Сумма: ${payment.final_amount_usd}\n\n"
                f"Доступ активирован! Проверь сообщения выше 👆\n\n"
                f"Спасибо за покупку! 💜",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ Не удалось уведомить пользователя {payment.user_id}: {e}")

        # Update admin message
        await callback.message.edit_text(
            f"✅ **ПЛАТЕЖ ПОДТВЕРЖДЕН**\n\n"
            f"Пользователь: {payment.user_id}\n"
            f"Продукт: {product_name}\n"
            f"Сумма: ${payment.final_amount_usd}\n\n"
            f"Доступ выдан!",
            parse_mode="Markdown"
        )
        await callback.answer("✅ Платеж подтвержден!")

    except ValueError:
        await callback.answer("❌ Неверный формат ID платежа", show_alert=True)
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data.startswith(CB_ADMIN_REJECT_PAYMENT))
async def reject_payment_button(callback: CallbackQuery, repo: RequestsRepo):
    """
    Reject pending payment via button click

    Callback data format: admin_reject_payment:PAYMENT_ID
    """
    try:
        # Parse payment_id from callback data
        payment_id = int(callback.data.split(":")[1])

        # Get payment
        payment = await repo.payments.get_payment_by_id(payment_id)

        if not payment:
            await callback.answer("❌ Платеж не найден", show_alert=True)
            return

        if payment.status != "pending":
            await callback.answer(f"❌ Платеж уже обработан (статус: {payment.status})", show_alert=True)
            return

        # Reject payment
        await repo.payments.reject_payment(payment.id)

        # Notify user about rejection
        product_name = PRODUCT_NAMES.get(payment.product_type, "продукт")

        try:
            await callback.bot.send_message(
                payment.user_id,
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
            print(f"❌ Не удалось уведомить пользователя {payment.user_id}: {e}")

        # Update admin message
        await callback.message.edit_text(
            f"❌ **ПЛАТЕЖ ОТКЛОНЕН**\n\n"
            f"Пользователь: {payment.user_id}\n"
            f"Продукт: {product_name}\n"
            f"Сумма: ${payment.final_amount_usd}\n\n"
            f"Пользователь уведомлен.",
            parse_mode="Markdown"
        )
        await callback.answer("❌ Платеж отклонен")

    except ValueError:
        await callback.answer("❌ Неверный формат ID платежа", show_alert=True)
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.message(Command("approve"))
async def approve_payment_command(message: Message, repo: RequestsRepo, settings):
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
            settings
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
