from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_menu, skip_keyboard, after_diagnostics_keyboard
from texts.messages import (
    MAIN_MENU,
    DIAGNOSTICS_ASK_BUSINESS,
    DIAGNOSTICS_ASK_AUTOMATION,
    DIAGNOSTICS_ASK_BUDGET,
    DIAGNOSTICS_RECOMMENDATION_SIMPLE,
    DIAGNOSTICS_RECOMMENDATION_MEDIUM,
    DIAGNOSTICS_RECOMMENDATION_COMPLEX,
    DIAGNOSTICS_SKIP,
    DIAGNOSTICS_DONE,
)
from utils.states import DiagnosticsStates
from database.db import (
    save_diagnostics,
    mark_user_not_new,
    activate_funnel,
    schedule_funnel_message,
)
from config import ADMIN_ID

router = Router()


@router.message(F.text == "✅ Пройти диагностику")
async def start_diagnostics(message: Message, state: FSMContext):
    """Начать диагностику"""
    await state.set_state(DiagnosticsStates.business)
    await message.answer(
        DIAGNOSTICS_ASK_BUSINESS,
        reply_markup=skip_keyboard()
    )


@router.message(F.text == "⏭ Пропустить")
async def skip_diagnostics(message: Message, state: FSMContext):
    """Пропустить диагностику"""
    await state.clear()
    user_id = message.from_user.id
    await mark_user_not_new(user_id)
    await message.answer(DIAGNOSTICS_SKIP, reply_markup=main_menu())


@router.message(DiagnosticsStates.business, F.text)
async def process_business(message: Message, state: FSMContext):
    """Диагностика: бизнес"""
    if message.text == "⏭ Пропустить":
        await state.clear()
        await mark_user_not_new(message.from_user.id)
        await message.answer(DIAGNOSTICS_SKIP, reply_markup=main_menu())
        return

    await state.update_data(business=message.text)
    await state.set_state(DiagnosticsStates.automation)
    await message.answer(
        DIAGNOSTICS_ASK_AUTOMATION,
        reply_markup=skip_keyboard()
    )


@router.message(DiagnosticsStates.automation, F.text)
async def process_automation(message: Message, state: FSMContext):
    """Диагностика: что автоматизировать"""
    if message.text == "⏭ Пропустить":
        await state.clear()
        await mark_user_not_new(message.from_user.id)
        await message.answer(DIAGNOSTICS_SKIP, reply_markup=main_menu())
        return

    await state.update_data(automation=message.text)
    await state.set_state(DiagnosticsStates.budget)
    await message.answer(
        DIAGNOSTICS_ASK_BUDGET,
        reply_markup=skip_keyboard()
    )


@router.message(DiagnosticsStates.budget, F.text)
async def process_budget(message: Message, state: FSMContext):
    """Диагностика: бюджет — финальный шаг"""
    if message.text == "⏭ Пропустить":
        await state.clear()
        await mark_user_not_new(message.from_user.id)
        await message.answer(DIAGNOSTICS_SKIP, reply_markup=main_menu())
        return

    await state.update_data(budget=message.text)
    data = await state.get_data()
    user = message.from_user

    budget_text = message.text.lower()
    if "100" in budget_text or "60" in budget_text:
        recommendation = "complex"
        rec_text = DIAGNOSTICS_RECOMMENDATION_COMPLEX
    elif "30" in budget_text or "50" in budget_text or "средн" in budget_text:
        recommendation = "medium"
        rec_text = DIAGNOSTICS_RECOMMENDATION_MEDIUM
    else:
        recommendation = "simple"
        rec_text = DIAGNOSTICS_RECOMMENDATION_SIMPLE

    try:
        await save_diagnostics(
            user_id=user.id,
            business=data.get('business', ''),
            automation=data.get('automation', ''),
            budget=data.get('budget', ''),
            recommendation=recommendation
        )
    except Exception as e:
        print(f"Ошибка сохранения диагностики: {e}")

    await mark_user_not_new(user.id)
    await activate_funnel(user.id)

    # Планируем сообщения воронки
    now = datetime.utcnow()
    steps = [
        (1, now + timedelta(hours=1)),
        (2, now + timedelta(days=1)),
        (3, now + timedelta(days=3)),
        (4, now + timedelta(days=7)),
    ]
    for step, scheduled_at in steps:
        try:
            await schedule_funnel_message(
                user_id=user.id,
                step=step,
                scheduled_at=scheduled_at.strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Ошибка планирования воронки (шаг {step}): {e}")

    # Уведомление админу
    contact = f"@{user.username}" if user.username else str(user.id)
    admin_message = (
        f"🔔 НОВЫЙ ЛИД (диагностика)\n\n"
        f"👤 {user.first_name or ''} ({contact})\n"
        f"💼 Бизнес: {data.get('business', '—')}\n"
        f"⚙️ Автоматизация: {data.get('automation', '—')}\n"
        f"💰 Бюджет: {data.get('budget', '—')}\n"
        f"📋 Рекомендация: {recommendation}\n\n"
        f"ID: {user.id}"
    )
    try:
        await message.bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    await state.clear()
    await message.answer(rec_text, reply_markup=after_diagnostics_keyboard())


@router.message(DiagnosticsStates.business)
@router.message(DiagnosticsStates.automation)
@router.message(DiagnosticsStates.budget)
async def diagnostics_non_text(message: Message):
    """Отклонить нетекстовые сообщения в FSM диагностики"""
    await message.answer("Пожалуйста, отправьте текстовое сообщение.")
