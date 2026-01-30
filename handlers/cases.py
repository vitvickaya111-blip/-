from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import cases_menu, main_menu
from texts.messages import CASES_MENU, CASE_FITNESS, CASE_EMIGRATION

router = Router()


@router.message(F.text == "💼 Мои кейсы")
async def cases(message: Message):
    """Меню кейсов"""
    await message.answer(
        CASES_MENU,
        reply_markup=cases_menu()
    )


@router.message(F.text == "🏋️ Фитнес-бот AN_SPORT")
async def case_fitness(message: Message):
    """Кейс фитнес-бота"""
    await message.answer(CASE_FITNESS, reply_markup=cases_menu())


@router.message(F.text == "✈️ Бот по эмиграции")
async def case_emigration(message: Message):
    """Кейс бота по эмиграции"""
    await message.answer(CASE_EMIGRATION, reply_markup=cases_menu())


@router.message(F.text == "🎯 Хочу такого же бота")
async def want_same_bot(message: Message):
    """Хочу такого же бота"""
    await message.answer(
        "Отлично! 🎯\n\n"
        "Напишите мне напрямую: @nastya\n\n"
        "Или оставьте заявку через 'Бесплатная консультация' в главном меню.\n\n"
        "Обсудим ваш проект!",
        reply_markup=main_menu()
    )
