from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_menu
from keyboards.inline import services_menu, education_menu
from texts.messages import get_main_menu, SERVICES_INTRO, EDUCATION_INTRO, CONSULTATION_INTRO
from database.db import (
    add_user, get_user, update_user_stage, get_stats,
    has_funnel_messages, schedule_funnel_message, reset_reactivation,
)
from config import ADMIN_ID

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    await state.clear()

    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or ""
    )

    user = await get_user(message.from_user.id)

    # Планируем прогревающую цепочку для новых пользователей
    user_id = message.from_user.id
    if not await has_funnel_messages(user_id):
        now = datetime.utcnow()
        steps = [
            (1, now + timedelta(hours=1)),
            (2, now + timedelta(days=1)),
            (3, now + timedelta(days=3)),
            (4, now + timedelta(days=7)),
        ]
        for step, scheduled_at in steps:
            await schedule_funnel_message(
                user_id=user_id,
                step=step,
                scheduled_at=scheduled_at.strftime('%Y-%m-%d %H:%M:%S')
            )

    # Сбросить флаг реактивации при повторном визите
    await reset_reactivation(user_id)

    welcome = get_main_menu(
        first_name=user['first_name'] if user else message.from_user.first_name,
        total=user['total_messages'] if user else 0
    )

    await message.answer(welcome, reply_markup=main_menu())


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика бота (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Эта команда только для админа")
        return

    stats = await get_stats()

    # Форматируем последних пользователей
    recent = ""
    for u in stats['recent_users']:
        username = f"@{u[0]}" if u[0] else "без username"
        recent += f"  • {u[1]} ({username})\n"

    text = f"""📊 СТАТИСТИКА БОТА

👥 Всего пользователей: {stats['total_users']}
🆕 Сегодня новых: {stats['today_users']}

💬 Заявок на консультацию: {stats['total_consultations']}
📝 Брифов: {stats['total_briefs']}

━━━━━━━━━━━━━━━━━━━━

🕐 Последние пользователи:
{recent}"""

    await message.answer(text)


@router.message(F.text == "◀️ В меню")
async def back_to_menu(message: Message, state: FSMContext):
    """Возврат в меню"""
    await state.clear()

    user = await get_user(message.from_user.id)

    welcome = get_main_menu(
        first_name=user['first_name'] if user else message.from_user.first_name,
        total=user['total_messages'] if user else 0
    )

    await message.answer(welcome, reply_markup=main_menu())


# === Callbacks от калькулятора ===

@router.callback_query(F.data == "calc_order")
async def cb_calc_order(callback: CallbackQuery):
    """Заказать после калькулятора"""
    await callback.message.answer(SERVICES_INTRO, reply_markup=services_menu())
    await callback.answer("Отлично! 🚀")
    await update_user_stage(callback.from_user.id, "interested_order")


@router.callback_query(F.data == "calc_consult")
async def cb_calc_consult(callback: CallbackQuery):
    """Консультация после калькулятора"""
    await callback.message.answer(CONSULTATION_INTRO, reply_markup=main_menu())
    await callback.answer("Отличный выбор! 💬")
    await update_user_stage(callback.from_user.id, "wants_consultation")


@router.callback_query(F.data == "calc_learn")
async def cb_calc_learn(callback: CallbackQuery):
    """Обучение после калькулятора"""
    await callback.message.answer(EDUCATION_INTRO, reply_markup=education_menu())
    await callback.answer("Супер! 🎓")
    await update_user_stage(callback.from_user.id, "wants_learn")


@router.callback_query(F.data == "calc_restart")
async def cb_calc_restart(callback: CallbackQuery, state: FSMContext):
    """Пересчитать калькулятор"""
    from utils.states import CalculatorStates
    from texts.messages import CALC_ASK_HOURS
    from keyboards.reply import cancel_kb

    await state.set_state(CalculatorStates.hours_per_day)
    await callback.message.answer("Пересчитываем! 🔄\n\n" + CALC_ASK_HOURS, reply_markup=cancel_kb())
    await callback.answer()
