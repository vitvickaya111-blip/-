from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

from keyboards.reply import main_menu
from keyboards.inline import case_actions
from texts.messages import CASES_INTRO, CASE_FITNESS, CASE_CURRENT_BOT
from database.db import update_user_stage

router = Router()


def cases_inline():
    """Инлайн меню кейсов"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Фитнес-бот", callback_data="case_fitness")],
        [InlineKeyboardButton(text="🤖 Бот-визитка", callback_data="case_current")]
    ])


@router.message(F.text == "💼 Кейсы")
async def cases(message: Message):
    """Меню кейсов"""
    await message.answer(CASES_INTRO, reply_markup=cases_inline())
    await update_user_stage(message.from_user.id, "viewing_cases")


# === Callbacks ===

@router.callback_query(F.data == "case_fitness")
async def cb_case_fitness(callback: CallbackQuery):
    try:
        await callback.message.edit_text(CASE_FITNESS, reply_markup=case_actions())
    except TelegramBadRequest:
        pass
    await callback.answer()


@router.callback_query(F.data == "case_current")
async def cb_case_current(callback: CallbackQuery):
    try:
        await callback.message.edit_text(CASE_CURRENT_BOT, reply_markup=case_actions())
    except TelegramBadRequest:
        pass
    await callback.answer()


@router.callback_query(F.data == "want_similar")
async def cb_want_similar(callback: CallbackQuery):
    await callback.message.answer(
        "Супер! 🎯\n\nНапишите: @bugivugi24\n\n"
        "Или через 'Консультация'\n\nСделаю такого же! 🚀",
        reply_markup=main_menu()
    )
    await callback.answer("Отлично! ✨")
    await update_user_stage(callback.from_user.id, "wants_similar")


@router.callback_query(F.data == "discuss_case")
async def cb_discuss_case(callback: CallbackQuery):
    await callback.message.answer(
        "Отлично! 💬\n\nНапишите: @bugivugi24\n\nОбсудим проект!",
        reply_markup=main_menu()
    )
    await callback.answer("Договорились! 🤝")


@router.callback_query(F.data == "back_cases")
async def cb_back_cases(callback: CallbackQuery):
    try:
        await callback.message.edit_text(CASES_INTRO, reply_markup=cases_inline())
    except TelegramBadRequest:
        pass
    await callback.answer()
