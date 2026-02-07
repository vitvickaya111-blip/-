from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.reply import main_menu
from database.db import save_brief
from config import ADMIN_ID
import json

router = Router()


class QuizStates(StatesGroup):
    """Состояния квиза"""
    contact = State()


def quiz_q1():
    """Первый вопрос квиза"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Приём заявок", callback_data="quiz_1_applications")],
        [InlineKeyboardButton(text="💰 Продажи", callback_data="quiz_1_sales")],
        [InlineKeyboardButton(text="👥 Работа с клиентами", callback_data="quiz_1_clients")],
        [InlineKeyboardButton(text="📊 Связка с таблицами/CRM", callback_data="quiz_1_crm")],
        [InlineKeyboardButton(text="🔧 Другое", callback_data="quiz_1_other")]
    ])


def quiz_q2():
    """Второй вопрос квиза"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 10к", callback_data="quiz_2_10k")],
        [InlineKeyboardButton(text="10-30к", callback_data="quiz_2_30k")],
        [InlineKeyboardButton(text="30к+", callback_data="quiz_2_more")],
        [InlineKeyboardButton(text="Нужна оценка", callback_data="quiz_2_estimate")]
    ])


QUIZ_INTRO = """🎯 ПОДБЕРУ РЕШЕНИЕ ПОД ТЕБЯ

Всего 3 вопроса — займёт 1 минуту.
После этого напишу с предложением!

━━━━━━━━━━━━━━━━━━━━

1️⃣ Что нужно автоматизировать?"""


@router.message(F.text == "🎯 Квиз")
async def quiz_start(message: Message):
    """Начало квиза"""
    await message.answer(QUIZ_INTRO, reply_markup=quiz_q1())


@router.callback_query(F.data.startswith("quiz_1_"))
async def quiz_answer1(callback: CallbackQuery, state: FSMContext):
    """Ответ на первый вопрос"""
    answer = callback.data.replace("quiz_1_", "")
    answers = {
        "applications": "Приём заявок",
        "sales": "Продажи",
        "clients": "Работа с клиентами",
        "crm": "Связка с таблицами/CRM",
        "other": "Другое"
    }
    await state.update_data(q1=answers.get(answer, answer))

    await callback.message.edit_text(
        f"✅ Понял: {answers.get(answer, answer)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "2️⃣ Сколько готов вложить?",
        reply_markup=quiz_q2()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_2_"))
async def quiz_answer2(callback: CallbackQuery, state: FSMContext):
    """Ответ на второй вопрос"""
    answer = callback.data.replace("quiz_2_", "")
    answers = {
        "10k": "До 10к",
        "30k": "10-30к",
        "more": "30к+",
        "estimate": "Нужна оценка"
    }
    await state.update_data(q2=answers.get(answer, answer))
    await state.set_state(QuizStates.contact)

    await callback.message.edit_text(
        f"✅ Бюджет: {answers.get(answer, answer)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "3️⃣ Как с тобой связаться?\n\n"
        "Напиши Telegram или WhatsApp:"
    )
    await callback.answer()


@router.message(QuizStates.contact)
async def quiz_contact(message: Message, state: FSMContext):
    """Получение контакта"""
    data = await state.get_data()
    data['contact'] = message.text

    user = message.from_user

    # Сохраняем в базу
    await save_brief(user.id, "квиз", json.dumps(data, ensure_ascii=False))

    # Отправляем админу
    admin_msg = (
        f"🎯 НОВЫЙ КВИЗ!\n\n"
        f"👤 {user.first_name} (@{user.username or user.id})\n\n"
        f"1️⃣ Задача: {data.get('q1', '?')}\n"
        f"2️⃣ Бюджет: {data.get('q2', '?')}\n"
        f"3️⃣ Контакт: {data.get('contact', '?')}\n\n"
        f"ID: {user.id}"
    )

    try:
        await message.bot.send_message(ADMIN_ID, admin_msg)
    except Exception as e:
        print(f"Ошибка: {e}")

    await state.clear()
    await message.answer(
        "✅ Принял!\n\n"
        "Напишу тебе в течение 2 часов с предложением.\n\n"
        "А пока можешь посмотреть:\n"
        "• 💼 Кейсы — что уже делала\n"
        "• 🤖 Заказать — все услуги",
        reply_markup=main_menu()
    )
