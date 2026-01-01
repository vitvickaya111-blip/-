from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.database.requests import RequestsRepo
from keyboards.inline import get_back_to_menu_keyboard
from utils.states import ConsultationForm

router = Router()


@router.message(F.text, ~F.text.startswith('/'))
async def handle_user_message(
        message: Message,
        state: FSMContext,
        repo: RequestsRepo,
        config
):
    """Handle direct messages from users (not in any state)"""

    # Check if user is in consultation form state
    current_state = await state.get_state()
    if current_state in [
        ConsultationForm.waiting_for_name.state,
        ConsultationForm.waiting_for_situation.state,
        ConsultationForm.waiting_for_concern.state,
        ConsultationForm.waiting_for_payment_screenshot.state
    ]:
        # Message will be handled by consultation form handlers
        return

    # Update last_message_date
    await repo.users.update(
        message.from_user.id,
        last_message_date=datetime.utcnow()
    )

    # Send auto-response
    response_text = """Получила твоё сообщение! 💌

Я отвечу тебе в течение 24 часов.

А пока можешь:
• Скачать мой гайд по Вьетнаму
• Подписаться на канал
• Посмотреть информацию о консультации"""

    await message.answer(response_text, reply_markup=get_back_to_menu_keyboard())

    # Notify admin about new message
    admin_ids = config.bot.admin_ids
    if admin_ids:
        from aiogram import Bot
        bot: Bot = message.bot
        for admin_id in admin_ids:
            try:
                notification_text = (
                    f"💬 Новое сообщение от пользователя!\n\n"
                    f"От: {message.from_user.first_name}"
                )
                if message.from_user.username:
                    notification_text += f" (@{message.from_user.username})"
                notification_text += f"\nID: {message.from_user.id}\n\n"
                notification_text += f"Сообщение:\n{message.text}"

                await bot.send_message(admin_id, notification_text)
            except Exception:
                pass
