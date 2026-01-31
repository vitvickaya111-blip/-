from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import consultation_menu, cancel_keyboard, main_menu
from texts.messages import (
    CONSULTATION_INTRO,
    CONSULTATION_ASK_NAME,
    CONSULTATION_ASK_BUSINESS,
    CONSULTATION_ASK_TASK,
    CONSULTATION_SUCCESS
)
from utils.states import ConsultationStates
from database.db import save_consultation, mark_consultation_booked
from config import ADMIN_ID

router = Router()


@router.message(F.text == "💬 Бесплатная консультация")
async def consultation(message: Message):
    """Меню консультации"""
    await message.answer(
        CONSULTATION_INTRO,
        reply_markup=consultation_menu()
    )


@router.message(F.text == "📅 Записаться на консультацию")
async def start_consultation(message: Message, state: FSMContext):
    """Начать запись на консультацию"""
    await state.set_state(ConsultationStates.name)
    await message.answer(
        CONSULTATION_ASK_NAME,
        reply_markup=cancel_keyboard()
    )


@router.message(ConsultationStates.name, F.text)
async def process_name(message: Message, state: FSMContext):
    """Обработка имени"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(name=message.text)
    await state.set_state(ConsultationStates.business)
    await message.answer(
        CONSULTATION_ASK_BUSINESS,
        reply_markup=cancel_keyboard()
    )


@router.message(ConsultationStates.business, F.text)
async def process_business(message: Message, state: FSMContext):
    """Обработка бизнеса"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(business=message.text)
    await state.set_state(ConsultationStates.task)
    await message.answer(
        CONSULTATION_ASK_TASK,
        reply_markup=cancel_keyboard()
    )


@router.message(ConsultationStates.task, F.text)
async def process_task(message: Message, state: FSMContext):
    """Обработка задачи"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(task=message.text)

    data = await state.get_data()
    user = message.from_user
    contact = f"@{user.username}" if user.username else str(user.id)

    try:
        await save_consultation(
            user_id=user.id,
            name=data['name'],
            business=data['business'],
            task=data['task'],
            contact=contact
        )
        await mark_consultation_booked(user.id)
    except Exception as e:
        print(f"Ошибка сохранения в БД: {e}")

    admin_message = (
        f"🔔 НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ\n\n"
        f"👤 Имя: {data['name']}\n"
        f"💼 Бизнес: {data['business']}\n"
        f"🎯 Задача: {data['task']}\n"
        f"📱 Контакт: {contact}\n\n"
        f"ID пользователя: {user.id}"
    )

    try:
        await message.bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    await state.clear()
    await message.answer(
        CONSULTATION_SUCCESS,
        reply_markup=main_menu()
    )


@router.message(ConsultationStates.name)
@router.message(ConsultationStates.business)
@router.message(ConsultationStates.task)
async def consultation_non_text(message: Message):
    """Отклонить нетекстовые сообщения в FSM"""
    await message.answer("Пожалуйста, отправьте текстовое сообщение.")


@router.message(F.text == "💬 Написать в личку")
async def write_direct(message: Message):
    """Написать в личку"""
    await message.answer(
        "Напишите мне напрямую: @nastya\n\n"
        "Отвечу в течение 24 часов!",
        reply_markup=main_menu()
    )
