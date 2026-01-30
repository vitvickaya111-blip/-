from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import (
    services_menu,
    telegram_bots_menu,
    cancel_keyboard,
    main_menu
)
from texts.messages import (
    SERVICES_MENU,
    TELEGRAM_BOTS,
    BOT_DEPLOY,
    BOT_SIMPLE,
    BOT_MEDIUM,
    BOT_COMPLEX,
    BRIEF_ASK_BUSINESS,
    BRIEF_ASK_TASK,
    BRIEF_ASK_FUNCTIONAL,
    BRIEF_ASK_PAYMENT,
    BRIEF_ASK_DEADLINE,
    BRIEF_ASK_BUDGET,
    BRIEF_SUCCESS
)
from utils.states import BriefBotStates
from database.db import save_brief
from config import ADMIN_ID

router = Router()


@router.message(F.text == "🤖 Заказать разработку")
async def services(message: Message):
    """Меню услуг"""
    await message.answer(
        SERVICES_MENU,
        reply_markup=services_menu()
    )


@router.message(F.text == "📱 Telegram-боты")
async def telegram_bots(message: Message):
    """Раздел Telegram-ботов"""
    await message.answer(
        TELEGRAM_BOTS,
        reply_markup=telegram_bots_menu()
    )


@router.message(F.text == "◀️ Назад к услугам")
async def back_to_services(message: Message):
    """Назад к услугам"""
    await message.answer(
        SERVICES_MENU,
        reply_markup=services_menu()
    )


@router.message(F.text == "🔧 Деплой бота - 8 000₽")
async def bot_deploy_info(message: Message):
    """Информация о деплое"""
    await message.answer(BOT_DEPLOY, reply_markup=telegram_bots_menu())


@router.message(F.text == "📱 Простой бот - 25 000₽")
async def bot_simple_info(message: Message):
    """Информация о простом боте"""
    await message.answer(BOT_SIMPLE, reply_markup=telegram_bots_menu())


@router.message(F.text == "🚀 Средний бот - 50 000₽")
async def bot_medium_info(message: Message):
    """Информация о среднем боте"""
    await message.answer(BOT_MEDIUM, reply_markup=telegram_bots_menu())


@router.message(F.text == "💎 Сложный бот - 100 000₽")
async def bot_complex_info(message: Message):
    """Информация о сложном боте"""
    await message.answer(BOT_COMPLEX, reply_markup=telegram_bots_menu())


@router.message(F.text == "📝 Заполнить бриф")
async def start_brief(message: Message, state: FSMContext):
    """Начать заполнение брифа"""
    await state.set_state(BriefBotStates.business)
    await message.answer(
        BRIEF_ASK_BUSINESS,
        reply_markup=cancel_keyboard()
    )


@router.message(BriefBotStates.business)
async def brief_business(message: Message, state: FSMContext):
    """Бриф: бизнес"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(business=message.text)
    await state.set_state(BriefBotStates.task)
    await message.answer(BRIEF_ASK_TASK, reply_markup=cancel_keyboard())


@router.message(BriefBotStates.task)
async def brief_task(message: Message, state: FSMContext):
    """Бриф: задача"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(task=message.text)
    await state.set_state(BriefBotStates.functional)
    await message.answer(BRIEF_ASK_FUNCTIONAL, reply_markup=cancel_keyboard())


@router.message(BriefBotStates.functional)
async def brief_functional(message: Message, state: FSMContext):
    """Бриф: функционал"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(functional=message.text)
    await state.set_state(BriefBotStates.payment)
    await message.answer(BRIEF_ASK_PAYMENT, reply_markup=cancel_keyboard())


@router.message(BriefBotStates.payment)
async def brief_payment(message: Message, state: FSMContext):
    """Бриф: оплата"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(payment=message.text)
    await state.set_state(BriefBotStates.deadline)
    await message.answer(BRIEF_ASK_DEADLINE, reply_markup=cancel_keyboard())


@router.message(BriefBotStates.deadline)
async def brief_deadline(message: Message, state: FSMContext):
    """Бриф: дедлайн"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(deadline=message.text)
    await state.set_state(BriefBotStates.budget)
    await message.answer(BRIEF_ASK_BUDGET, reply_markup=cancel_keyboard())


@router.message(BriefBotStates.budget)
async def brief_budget(message: Message, state: FSMContext):
    """Бриф: бюджет — финальный шаг"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(budget=message.text)
    data = await state.get_data()
    user = message.from_user

    # Сохранить в БД
    brief_text = (
        f"Бизнес: {data['business']}\n"
        f"Задача: {data['task']}\n"
        f"Функционал: {data['functional']}\n"
        f"Оплата в боте: {data['payment']}\n"
        f"Дедлайн: {data['deadline']}\n"
        f"Бюджет: {data['budget']}"
    )
    await save_brief(user_id=user.id, brief_type="telegram_bot", data=brief_text)

    # Отправить админу
    admin_message = (
        f"📋 НОВЫЙ БРИФ НА БОТА\n\n"
        f"👤 От: {user.first_name or ''} (@{user.username or user.id})\n\n"
        f"💼 Бизнес: {data['business']}\n"
        f"🎯 Задача: {data['task']}\n"
        f"⚙️ Функционал: {data['functional']}\n"
        f"💳 Оплата в боте: {data['payment']}\n"
        f"⏱ Дедлайн: {data['deadline']}\n"
        f"💰 Бюджет: {data['budget']}\n\n"
        f"ID: {user.id}"
    )

    try:
        await message.bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    await state.clear()
    await message.answer(BRIEF_SUCCESS, reply_markup=main_menu())


@router.message(F.text == "💬 Обсудить проект")
async def discuss_project(message: Message):
    """Обсудить проект"""
    await message.answer(
        "Отлично! Напишите мне напрямую: @nastya\n\n"
        "Или оставьте заявку через 'Бесплатная консультация' в главном меню.",
        reply_markup=main_menu()
    )


@router.message(F.text.in_([
    "🌐 Сайты и лендинги",
    "💻 Веб-приложения",
    "🔗 Интеграции и автоматизация",
    "📊 Автопостинг контента",
    "🧠 AI-ассистенты"
]))
async def other_services(message: Message):
    """Остальные услуги (заглушка)"""
    service_name = message.text.split()[1] if len(message.text.split()) > 1 else "эта услуга"
    await message.answer(
        f"Раздел '{message.text}' в разработке.\n\n"
        f"Хотите обсудить {service_name.lower()}?\n"
        f"Напишите мне: @nastya\n\n"
        f"Или оставьте заявку через 'Бесплатная консультация'.",
        reply_markup=services_menu()
    )
