import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database.db import get_all_users
from utils.states import BroadcastStates

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    """Команда /broadcast — начало рассылки (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(BroadcastStates.waiting_for_message)
    cancel_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отменить рассылку")]],
        resize_keyboard=True
    )
    await message.answer(
        "📨 Отправьте сообщение для рассылки всем пользователям.\n"
        "Можно отправить текст, фото, видео — любой контент.",
        reply_markup=cancel_kb
    )


@router.message(BroadcastStates.waiting_for_message, F.text == "❌ Отменить рассылку")
async def cancel_broadcast(message: Message, state: FSMContext):
    """Отмена рассылки"""
    await state.clear()
    await message.answer("Рассылка отменена.", reply_markup=ReplyKeyboardRemove())


@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext):
    """Принять сообщение и разослать всем пользователям"""
    await state.clear()

    users = await get_all_users()
    total = len(users)
    sent = 0
    failed = 0

    await message.answer(
        f"⏳ Начинаю рассылку для {total} пользователей...",
        reply_markup=ReplyKeyboardRemove()
    )

    for user_id in users:
        try:
            await message.bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await message.answer(
        f"✅ Рассылка завершена!\n\n"
        f"📬 Доставлено: {sent}\n"
        f"🚫 Не доставлено: {failed}\n"
        f"👥 Всего: {total}"
    )
    logger.info(f"Broadcast finished: sent={sent}, failed={failed}, total={total}")
