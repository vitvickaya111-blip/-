from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# === КАЛЬКУЛЯТОР ===

def calc_actions():
    """Действия после калькулятора"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Заказать", callback_data="calc_order")],
        [InlineKeyboardButton(text="💬 Консультация", callback_data="calc_consult")],
        [InlineKeyboardButton(text="🎓 Научиться", callback_data="calc_learn")],
        [InlineKeyboardButton(text="🔄 Пересчитать", callback_data="calc_restart")]
    ])


# === УСЛУГИ ===

def services_menu():
    """Меню услуг"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Боты", callback_data="srv_bots")],
        [InlineKeyboardButton(text="🌐 Сайты", callback_data="srv_sites")],
        [InlineKeyboardButton(text="💻 Веб-приложения", callback_data="srv_webapps")],
        [InlineKeyboardButton(text="🔗 Интеграции", callback_data="srv_integrations")],
        [InlineKeyboardButton(text="🤖 Автоматизация", callback_data="srv_automation")],
        [InlineKeyboardButton(text="🧠 AI-решения", callback_data="srv_ai")],
        [InlineKeyboardButton(text="🎨 Дизайн", callback_data="srv_design")]
    ])


def bots_packages():
    """Пакеты ботов"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Простой — 25к", callback_data="bot_simple")],
        [InlineKeyboardButton(text="🚀 Средний — 50к", callback_data="bot_medium")],
        [InlineKeyboardButton(text="💎 Сложный — 100к", callback_data="bot_complex")],
        [InlineKeyboardButton(text="🔧 Деплой — 8к", callback_data="bot_deploy")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def sites_packages():
    """Пакеты сайтов"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Лендинг — 30к", callback_data="site_landing")],
        [InlineKeyboardButton(text="🌐 Сайт 5стр — 50к", callback_data="site_small")],
        [InlineKeyboardButton(text="🏢 Сайт 10стр — 80к", callback_data="site_medium")],
        [InlineKeyboardButton(text="🛒 Магазин — 100к", callback_data="site_shop")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def webapps_packages():
    """Пакеты веб-приложений"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Калькулятор — 20к", callback_data="webapp_calc")],
        [InlineKeyboardButton(text="📋 Форма — 30к", callback_data="webapp_form")],
        [InlineKeyboardButton(text="👤 Кабинет — 60к", callback_data="webapp_cabinet")],
        [InlineKeyboardButton(text="💼 CRM — 150к", callback_data="webapp_crm")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def integrations_packages():
    """Пакеты интеграций"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Бот+Сайт — 15к", callback_data="int_botsite")],
        [InlineKeyboardButton(text="💼 Бот+CRM — 25к", callback_data="int_botcrm")],
        [InlineKeyboardButton(text="💳 Платежи — 20к", callback_data="int_payments")],
        [InlineKeyboardButton(text="📊 Sheets — 15к", callback_data="int_sheets")],
        [InlineKeyboardButton(text="✉️ Email — 15к", callback_data="int_email")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def automation_packages():
    """Пакеты автоматизации"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Автопостинг — 25к", callback_data="auto_posting")],
        [InlineKeyboardButton(text="🔍 Парсинг — 30к", callback_data="auto_parsing")],
        [InlineKeyboardButton(text="📊 Таблицы — 20к", callback_data="auto_sheets")],
        [InlineKeyboardButton(text="✉️ Рассылки — 20к", callback_data="auto_mailing")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def ai_packages():
    """Пакеты AI"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 AI-чатбот — 50к", callback_data="ai_chatbot")],
        [InlineKeyboardButton(text="✍️ Контент — 40к", callback_data="ai_content")],
        [InlineKeyboardButton(text="🤖 Ассистент — 80к", callback_data="ai_assistant")],
        [InlineKeyboardButton(text="📊 Анализ — 60к", callback_data="ai_analytics")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def design_packages():
    """Пакеты дизайна"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Презентация 10 — 15к", callback_data="design_pres10")],
        [InlineKeyboardButton(text="📊 Презентация 30 — 30к", callback_data="design_pres30")],
        [InlineKeyboardButton(text="🎨 Дизайн сайта — 25к", callback_data="design_site")],
        [InlineKeyboardButton(text="📱 10 постов — 10к", callback_data="design_posts")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_services")]
    ])


def package_actions(code: str):
    """Действия после описания пакета"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Заказать!", callback_data=f"order_{code}")],
        [InlineKeyboardButton(text="💬 Вопрос", callback_data="ask_q")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_category")]
    ])


# === ОБУЧЕНИЕ ===

def education_menu():
    """Меню обучения"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Создание ботов", callback_data="edu_bots")],
        [InlineKeyboardButton(text="🌐 Создание сайтов", callback_data="edu_sites")]
    ])


def workshop_actions():
    """Действия после описания воркшопа"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Записаться!", callback_data="ws_register")],
        [InlineKeyboardButton(text="💬 Вопрос", callback_data="ws_question")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="ws_back")]
    ])


# === КЕЙСЫ ===

def case_actions():
    """Действия после кейса"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Хочу такого!", callback_data="want_similar")],
        [InlineKeyboardButton(text="💬 Обсудить", callback_data="discuss_case")],
        [InlineKeyboardButton(text="◀️ К кейсам", callback_data="back_cases")]
    ])
