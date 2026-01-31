from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤖 Заказать разработку")],
            [KeyboardButton(text="🎓 Научиться самому")],
            [KeyboardButton(text="💼 Мои кейсы")],
            [KeyboardButton(text="💬 Бесплатная консультация")],
            [KeyboardButton(text="👤 Обо мне")]
        ],
        resize_keyboard=True
    )
    return keyboard


def services_menu():
    """Меню услуг"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telegram-боты")],
            [KeyboardButton(text="🌐 Сайты и лендинги")],
            [KeyboardButton(text="💻 Веб-приложения")],
            [KeyboardButton(text="🔗 Интеграции и автоматизация")],
            [KeyboardButton(text="📊 Автопостинг контента")],
            [KeyboardButton(text="🧠 AI-ассистенты")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


def telegram_bots_menu():
    """Меню Telegram-ботов"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔧 Деплой бота - 8 000₽")],
            [KeyboardButton(text="📱 Простой бот - 25 000₽")],
            [KeyboardButton(text="🚀 Средний бот - 50 000₽")],
            [KeyboardButton(text="💎 Сложный бот - 100 000₽")],
            [KeyboardButton(text="📝 Заполнить бриф")],
            [KeyboardButton(text="💬 Обсудить проект")],
            [KeyboardButton(text="◀️ Назад к услугам")]
        ],
        resize_keyboard=True
    )
    return keyboard


def education_menu():
    """Меню обучения"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤖 Создание Telegram-ботов")],
            [KeyboardButton(text="🌐 Создание сайтов с AI")],
            [KeyboardButton(text="📊 Автопостинг и автоматизация")],
            [KeyboardButton(text="🧠 Работа с AI")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


def education_bots_menu():
    """Меню обучения ботам"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Первый бот за 4 часа - 5 000₽")],
            [KeyboardButton(text="📱 Бот-визитка - 7 000₽")],
            [KeyboardButton(text="🚀 Интенсив 7 дней - 15 000₽")],
            [KeyboardButton(text="📖 Воркшоп по деплою - 3 000₽")],
            [KeyboardButton(text="💎 Комбо-пакет - 35 000₽")],
            [KeyboardButton(text="◀️ Назад к обучению")]
        ],
        resize_keyboard=True
    )
    return keyboard


def cases_menu():
    """Меню кейсов"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏋️ Фитнес-бот AN_SPORT")],
            [KeyboardButton(text="✈️ Бот по эмиграции")],
            [KeyboardButton(text="🎯 Хочу такого же бота")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


def consultation_menu():
    """Меню консультации"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться на консультацию")],
            [KeyboardButton(text="💬 Написать в личку")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


def back_to_menu():
    """Кнопка назад в меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


def cancel_keyboard():
    """Кнопка отмены"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True
    )
    return keyboard


def diagnostics_start_keyboard():
    """Клавиатура начала диагностики"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Пройти диагностику")],
            [KeyboardButton(text="⏭ Пропустить")]
        ],
        resize_keyboard=True
    )
    return keyboard


def skip_keyboard():
    """Кнопка пропуска во время диагностики"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ Пропустить")]
        ],
        resize_keyboard=True
    )
    return keyboard
