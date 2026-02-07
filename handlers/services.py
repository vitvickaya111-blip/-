from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
import json
import logging

logger = logging.getLogger(__name__)

from keyboards.reply import main_menu, cancel_kb
from keyboards.inline import (
    services_menu, bots_packages, sites_packages, webapps_packages,
    integrations_packages, automation_packages, ai_packages,
    design_packages, package_actions
)
from texts.messages import (
    SERVICES_INTRO,
    BOT_DEPLOY, BOT_SIMPLE, BOT_MEDIUM, BOT_COMPLEX,
    SITE_LANDING, SITE_SMALL, SITE_MEDIUM, SITE_SHOP,
    WEBAPP_CALC, WEBAPP_FORM, WEBAPP_CABINET, WEBAPP_CRM,
    INT_BOTSITE, INT_BOTCRM, INT_PAYMENTS, INT_SHEETS, INT_EMAIL,
    AUTO_POSTING, AUTO_PARSING, AUTO_SHEETS, AUTO_MAILING,
    AI_CHATBOT, AI_CONTENT, AI_ASSISTANT, AI_ANALYTICS,
    DESIGN_PRES10, DESIGN_PRES30, DESIGN_SITE, DESIGN_POSTS,
    BRIEF_ASK_BUSINESS, BRIEF_ASK_TASK, BRIEF_ASK_FUNCTIONAL,
    BRIEF_ASK_PAYMENT, BRIEF_ASK_DEADLINE, BRIEF_ASK_BUDGET,
    get_brief_success
)
from utils.states import BriefStates
from utils.helpers import get_progress_bar
from database.db import save_brief, get_user, update_user_stage
from config import ADMIN_ID

router = Router()


# === ГЛАВНОЕ МЕНЮ УСЛУГ ===

@router.message(F.text == "🤖 Заказать")
async def services(message: Message):
    """Меню услуг"""
    await message.answer(SERVICES_INTRO, reply_markup=services_menu())
    await update_user_stage(message.from_user.id, "viewing_services")


# === CALLBACKS КАТЕГОРИЙ ===

@router.callback_query(F.data == "srv_bots")
async def cb_bots(callback: CallbackQuery):
    await callback.message.edit_text("📱 TELEGRAM-БОТЫ\n\nВыберите пакет:", reply_markup=bots_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_sites")
async def cb_sites(callback: CallbackQuery):
    await callback.message.edit_text("🌐 САЙТЫ\n\nВыберите пакет:", reply_markup=sites_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_webapps")
async def cb_webapps(callback: CallbackQuery):
    await callback.message.edit_text("💻 ВЕБ-ПРИЛОЖЕНИЯ\n\nВыберите пакет:", reply_markup=webapps_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_integrations")
async def cb_integrations(callback: CallbackQuery):
    await callback.message.edit_text("🔗 ИНТЕГРАЦИИ\n\nВыберите пакет:", reply_markup=integrations_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_automation")
async def cb_automation(callback: CallbackQuery):
    await callback.message.edit_text("🤖 АВТОМАТИЗАЦИЯ\n\nВыберите пакет:", reply_markup=automation_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_ai")
async def cb_ai(callback: CallbackQuery):
    await callback.message.edit_text("🧠 AI-РЕШЕНИЯ\n\nВыберите пакет:", reply_markup=ai_packages())
    await callback.answer()


@router.callback_query(F.data == "srv_design")
async def cb_design(callback: CallbackQuery):
    await callback.message.edit_text("🎨 ДИЗАЙН\n\nВыберите пакет:", reply_markup=design_packages())
    await callback.answer()


@router.callback_query(F.data == "back_services")
async def cb_back_services(callback: CallbackQuery):
    try:
        await callback.message.edit_text(SERVICES_INTRO, reply_markup=services_menu())
    except TelegramBadRequest:
        pass
    await callback.answer()


# === CALLBACKS ПАКЕТОВ — БОТЫ ===

PACKAGES_INFO = {
    # Боты
    "bot_simple": (BOT_SIMPLE, "simple", bots_packages),
    "bot_medium": (BOT_MEDIUM, "medium", bots_packages),
    "bot_complex": (BOT_COMPLEX, "complex", bots_packages),
    "bot_deploy": (BOT_DEPLOY, "deploy", bots_packages),
    # Сайты
    "site_landing": (SITE_LANDING, "landing", sites_packages),
    "site_small": (SITE_SMALL, "site_small", sites_packages),
    "site_medium": (SITE_MEDIUM, "site_medium", sites_packages),
    "site_shop": (SITE_SHOP, "shop", sites_packages),
    # Веб-приложения
    "webapp_calc": (WEBAPP_CALC, "webapp_calc", webapps_packages),
    "webapp_form": (WEBAPP_FORM, "webapp_form", webapps_packages),
    "webapp_cabinet": (WEBAPP_CABINET, "webapp_cabinet", webapps_packages),
    "webapp_crm": (WEBAPP_CRM, "webapp_crm", webapps_packages),
    # Интеграции
    "int_botsite": (INT_BOTSITE, "int_botsite", integrations_packages),
    "int_botcrm": (INT_BOTCRM, "int_botcrm", integrations_packages),
    "int_payments": (INT_PAYMENTS, "int_payments", integrations_packages),
    "int_sheets": (INT_SHEETS, "int_sheets", integrations_packages),
    "int_email": (INT_EMAIL, "int_email", integrations_packages),
    # Автоматизация
    "auto_posting": (AUTO_POSTING, "auto_posting", automation_packages),
    "auto_parsing": (AUTO_PARSING, "auto_parsing", automation_packages),
    "auto_sheets": (AUTO_SHEETS, "auto_sheets", automation_packages),
    "auto_mailing": (AUTO_MAILING, "auto_mailing", automation_packages),
    # AI
    "ai_chatbot": (AI_CHATBOT, "ai_chatbot", ai_packages),
    "ai_content": (AI_CONTENT, "ai_content", ai_packages),
    "ai_assistant": (AI_ASSISTANT, "ai_assistant", ai_packages),
    "ai_analytics": (AI_ANALYTICS, "ai_analytics", ai_packages),
    # Дизайн
    "design_pres10": (DESIGN_PRES10, "design_pres10", design_packages),
    "design_pres30": (DESIGN_PRES30, "design_pres30", design_packages),
    "design_site": (DESIGN_SITE, "design_site", design_packages),
    "design_posts": (DESIGN_POSTS, "design_posts", design_packages),
}

# Маппинг категорий для кнопки "Назад"
CATEGORY_KEYBOARDS = {
    "bot_": bots_packages,
    "site_": sites_packages,
    "webapp_": webapps_packages,
    "int_": integrations_packages,
    "auto_": automation_packages,
    "ai_": ai_packages,
    "design_": design_packages,
}


@router.callback_query(F.data.in_(PACKAGES_INFO.keys()))
async def cb_package(callback: CallbackQuery, state: FSMContext):
    info = PACKAGES_INFO[callback.data]
    text, code, _ = info
    await state.update_data(current_package=code)
    await callback.message.edit_text(text, reply_markup=package_actions(code))
    await callback.answer()


@router.callback_query(F.data == "back_category")
async def cb_back_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    code = data.get("current_package", "")

    # Определяем категорию по коду пакета
    kb_func = services_menu
    title = "Выберите категорию:"

    if code.startswith("simple") or code.startswith("medium") or code.startswith("complex") or code.startswith("deploy"):
        kb_func = bots_packages
        title = "📱 TELEGRAM-БОТЫ\n\nВыберите пакет:"
    elif code.startswith("landing") or code.startswith("site_") or code.startswith("shop"):
        kb_func = sites_packages
        title = "🌐 САЙТЫ\n\nВыберите пакет:"
    elif code.startswith("webapp"):
        kb_func = webapps_packages
        title = "💻 ВЕБ-ПРИЛОЖЕНИЯ\n\nВыберите пакет:"
    elif code.startswith("int_"):
        kb_func = integrations_packages
        title = "🔗 ИНТЕГРАЦИИ\n\nВыберите пакет:"
    elif code.startswith("auto_"):
        kb_func = automation_packages
        title = "🤖 АВТОМАТИЗАЦИЯ\n\nВыберите пакет:"
    elif code.startswith("ai_"):
        kb_func = ai_packages
        title = "🧠 AI-РЕШЕНИЯ\n\nВыберите пакет:"
    elif code.startswith("design_"):
        kb_func = design_packages
        title = "🎨 ДИЗАЙН\n\nВыберите пакет:"

    try:
        await callback.message.edit_text(title, reply_markup=kb_func())
    except TelegramBadRequest:
        pass
    await callback.answer()


# === ЗАКАЗ И БРИФ ===

@router.callback_query(F.data.startswith("order_"))
async def cb_order(callback: CallbackQuery, state: FSMContext):
    package = callback.data.replace("order_", "")
    await state.set_state(BriefStates.business)
    await state.update_data(package=package)
    logger.info(f"[BRIEF] state set to business, package: {package}")

    user = await get_user(callback.from_user.id)
    first_name = user['first_name'] if user else callback.from_user.first_name

    await callback.message.answer(
        f"Отлично, {first_name}! 🎉\n\nБриф — 6 вопросов.\n\n{BRIEF_ASK_BUSINESS}",
        reply_markup=cancel_kb()
    )
    await callback.answer("Начинаем! 🚀")
    await update_user_stage(callback.from_user.id, f"ordering_{package}")


@router.callback_query(F.data == "ask_q")
async def cb_ask_q(callback: CallbackQuery):
    await callback.message.edit_text(
        "💬 ВОПРОСЫ\n\nНапишите ваш вопрос мне: @bugivugi24"
    )
    await callback.answer()


# === БРИФ FSM ===

@router.message(StateFilter(BriefStates.business))
async def brief_business(message: Message, state: FSMContext):
    logger.info(f"[BRIEF] business handler triggered, text: {message.text[:50] if message.text else 'None'}")
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(business=message.text)
    await state.set_state(BriefStates.task)
    logger.info("[BRIEF] moving to task state")
    await message.answer(f"{get_progress_bar(1, 6)}\n\n{BRIEF_ASK_TASK}", reply_markup=cancel_kb())


@router.message(StateFilter(BriefStates.task))
async def brief_task(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(task=message.text)
    await state.set_state(BriefStates.functional)
    await message.answer(f"{get_progress_bar(2, 6)}\n\n{BRIEF_ASK_FUNCTIONAL}", reply_markup=cancel_kb())


@router.message(StateFilter(BriefStates.functional))
async def brief_functional(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(functional=message.text)
    await state.set_state(BriefStates.payment)
    await message.answer(f"{get_progress_bar(3, 6)}\n\n{BRIEF_ASK_PAYMENT}", reply_markup=cancel_kb())


@router.message(StateFilter(BriefStates.payment))
async def brief_payment(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(payment=message.text)
    await state.set_state(BriefStates.deadline)
    await message.answer(f"{get_progress_bar(4, 6)}\n\n{BRIEF_ASK_DEADLINE}", reply_markup=cancel_kb())


@router.message(StateFilter(BriefStates.deadline))
async def brief_deadline(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return
    await state.update_data(deadline=message.text)
    await state.set_state(BriefStates.budget)
    await message.answer(f"{get_progress_bar(5, 6)}\n\n{BRIEF_ASK_BUDGET}", reply_markup=cancel_kb())


@router.message(StateFilter(BriefStates.budget))
async def brief_budget(message: Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    await state.update_data(budget=message.text)
    data = await state.get_data()
    user = message.from_user
    user_data = await get_user(user.id)
    first_name = user_data['first_name'] if user_data else user.first_name or "друг"

    await message.answer(f"{get_progress_bar(6, 6)}\n\nОбрабатываю... ⏳")

    await save_brief(user.id, "заказ", json.dumps(data, ensure_ascii=False))

    package = data.get('package', 'не указан')
    admin_msg = (
        f"🔔 НОВЫЙ БРИФ!\n\n"
        f"👤 {first_name}\n"
        f"📱 @{user.username if user.username else user.id}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 Пакет: {package}\n\n"
        f"💼 Бизнес:\n{data['business']}\n\n"
        f"🎯 Задача:\n{data['task']}\n\n"
        f"⚙️ Функционал:\n{data['functional']}\n\n"
        f"💳 Оплата: {data['payment']}\n"
        f"⏰ Срок: {data['deadline']}\n"
        f"💰 Бюджет: {data['budget']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"ID: {user.id}"
    )

    try:
        await message.bot.send_message(ADMIN_ID, admin_msg)
    except Exception as e:
        logger.error(f"Ошибка: {e}")

    await state.clear()
    await message.answer(get_brief_success(first_name), reply_markup=main_menu())
    await update_user_stage(user.id, "brief_completed")
