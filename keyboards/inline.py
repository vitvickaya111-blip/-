from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_education_buttons():
    """Инлайн-кнопки для меню обучения"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Воркшопы по ботам", callback_data="edu_bots")],
        [InlineKeyboardButton(text="🌐 Воркшопы по сайтам", callback_data="edu_sites")],
        [InlineKeyboardButton(text="📊 Автопостинг", callback_data="edu_autopost")],
        [InlineKeyboardButton(text="🧠 AI-инструменты", callback_data="edu_ai")]
    ])
    return keyboard


def get_workshop_list():
    """Список воркшопов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ 4 часа — 5 000₽ 🔥", callback_data="ws_4h")],
        [InlineKeyboardButton(text="📱 Выходные — 7 000₽", callback_data="ws_weekend")],
        [InlineKeyboardButton(text="🚀 Интенсив — 15 000₽", callback_data="ws_intensive")],
        [InlineKeyboardButton(text="💎 Комбо — 35 000₽", callback_data="ws_combo")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_education")]
    ])
    return keyboard


def get_workshop_actions():
    """Действия после описания воркшопа"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Записаться!", callback_data="register_workshop")],
        [InlineKeyboardButton(text="💬 Задать вопрос", callback_data="ask_workshop_q")],
        [InlineKeyboardButton(text="◀️ К воркшопам", callback_data="back_to_workshops")]
    ])
    return keyboard


def get_package_actions(package: str):
    """Действия для пакета бота"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Заказать!", callback_data=f"order_{package}")],
        [InlineKeyboardButton(text="📝 Бриф", callback_data="start_brief")],
        [InlineKeyboardButton(text="💬 Вопрос", callback_data="ask_package_q")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_packages")]
    ])
    return keyboard


def get_case_actions():
    """Действия после кейса"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Хочу такого же!", callback_data="want_similar")],
        [InlineKeyboardButton(text="💬 Обсудить", callback_data="discuss_case")],
        [InlineKeyboardButton(text="◀️ К кейсам", callback_data="back_to_cases")]
    ])
    return keyboard


def get_calculator_actions():
    """Действия после калькулятора"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Хочу бота!", callback_data="calc_want_bot")],
        [InlineKeyboardButton(text="💬 Консультация", callback_data="calc_consultation")],
        [InlineKeyboardButton(text="🎓 Научиться", callback_data="calc_learn")],
        [InlineKeyboardButton(text="🔄 Пересчитать", callback_data="calc_restart")]
    ])
    return keyboard
