from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    """Главное меню"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📋 Чек-лист"), KeyboardButton(text="🎯 Квиз")],
        [KeyboardButton(text="🤖 Заказать"), KeyboardButton(text="🎓 Научиться")],
        [KeyboardButton(text="💼 Кейсы"), KeyboardButton(text="💬 Консультация")],
        [KeyboardButton(text="🧮 Калькулятор"), KeyboardButton(text="👤 Обо мне")]
    ], resize_keyboard=True)


def cancel_kb():
    """Клавиатура отмены"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="❌ Отменить")]
    ], resize_keyboard=True)
