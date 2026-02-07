from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import cancel_kb, main_menu
from texts.messages import (
    CONSULTATION_INTRO, CONSULTATION_ASK_NAME,
    CONSULTATION_ASK_BUSINESS, CONSULTATION_ASK_TASK,
    CONSULTATION_SUCCESS
)
from utils.states import ConsultationStates
from database.db import save_consultation, get_user, update_user_stage
from config import ADMIN_ID
from utils.helpers import get_progress_bar

router = Router()


@router.message(F.text == "💬 Консультация")
async def consultation(message: Message, state: FSMContext):
    """Меню консультации — сразу начинаем запись"""
    await state.set_state(ConsultationStates.name)
    print("[CONSULT] state set to name")
    await message.answer(
        CONSULTATION_INTRO + "\n\n" + CONSULTATION_ASK_NAME,
        reply_markup=cancel_kb()
    )
    await update_user_stage(message.from_user.id, "viewing_consultation")


@router.message(ConsultationStates.name)
async def process_name(message: Message, state: FSMContext):
    print(f"[CONSULT] name handler triggered, text: {message.text}")
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(name=message.text)
    await state.set_state(ConsultationStates.business)
    print("[CONSULT] moving to business state")

    await message.answer(
        f"Приятно познакомиться, {message.text}! 😊\n\n"
        f"{get_progress_bar(1, 3)}\n\n{CONSULTATION_ASK_BUSINESS}",
        reply_markup=cancel_kb()
    )


@router.message(ConsultationStates.business)
async def process_business(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(business=message.text)
    await state.set_state(ConsultationStates.task)

    await message.answer(
        f"Понятно! 👍\n\n{get_progress_bar(2, 3)}\n\n{CONSULTATION_ASK_TASK}",
        reply_markup=cancel_kb()
    )


@router.message(ConsultationStates.task)
async def process_task(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(task=message.text)
    data = await state.get_data()
    user = message.from_user
    user_data = await get_user(user.id)
    contact = f"@{user.username}" if user.username else str(user.id)

    await message.answer(f"{get_progress_bar(3, 3)}\n\nОбрабатываю... ⏳")

    await save_consultation(
        user_id=user.id,
        name=data['name'],
        business=data['business'],
        task=data['task'],
        contact=contact
    )

    admin_msg = (
        f"🔔 НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ!\n\n"
        f"👤 {data['name']} ({contact})\n\n"
        f"💼 Бизнес: {data['business']}\n"
        f"🎯 Задача: {data['task']}\n\n"
        f"ID: {user.id}\n"
        f"Этап: {user_data['stage'] if user_data else 'new'}"
    )

    try:
        await message.bot.send_message(ADMIN_ID, admin_msg)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    await state.clear()
    await message.answer(CONSULTATION_SUCCESS, reply_markup=main_menu())
    await update_user_stage(user.id, "consultation_requested")


@router.message(F.text == "💬 Написать")
async def write_direct(message: Message):
    """Написать напрямую"""
    await message.answer(
        "Пишите: @bugivugi24\n\nОтвечу в течение 24 часов! 😊",
        reply_markup=main_menu()
    )
