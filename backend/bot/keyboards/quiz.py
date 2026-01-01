"""Keyboards and callback data for quiz"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Callback data для квиза
CB_START_QUIZ = "start_quiz"
CB_ABOUT_ME = "about_me"
CB_BACK_FROM_STORY = "back_from_story"

# Question 1
CB_Q1_A = "q1_a"  # Отношения
CB_Q1_B = "q1_b"  # Работа
CB_Q1_C = "q1_c"  # Жизнь проходит мимо
CB_Q1_D = "q1_d"  # Финансы

# Question 2
CB_Q2_A = "q2_a"  # Несколько недель
CB_Q2_B = "q2_b"  # Несколько месяцев
CB_Q2_C = "q2_c"  # Больше года
CB_Q2_D = "q2_d"  # Постоянная мысль

# Question 3
CB_Q3_A = "q3_a"  # Страх
CB_Q3_B = "q3_b"  # Нет денег
CB_Q3_C = "q3_c"  # Мнение близких
CB_Q3_D = "q3_d"  # Не знаю с чего начать

# Question 4
CB_Q4_A = "q4_a"  # Да, готов
CB_Q4_B = "q4_b"  # Да, скоро истечёт
CB_Q4_C = "q4_c"  # Нет, планирую
CB_Q4_D = "q4_d"  # Нет, не думала

# Question 5
CB_Q5_A = "q5_a"  # Свободно
CB_Q5_B = "q5_b"  # Базовый
CB_Q5_C = "q5_c"  # Учу сейчас
CB_Q5_D = "q5_d"  # Совсем не знаю

# Question 6
CB_Q6_A = "q6_a"  # До 100к
CB_Q6_B = "q6_b"  # 100-300к
CB_Q6_C = "q6_c"  # 300-500к
CB_Q6_D = "q6_d"  # Больше 500к

# Question 7
CB_Q7_A = "q7_a"  # Тропики
CB_Q7_B = "q7_b"  # 4 сезона
CB_Q7_C = "q7_c"  # Умеренный
CB_Q7_D = "q7_d"  # Всё равно

# Question 8
CB_Q8_A = "q8_a"  # Безопасность
CB_Q8_B = "q8_b"  # Заработок
CB_Q8_C = "q8_c"  # Качество жизни
CB_Q8_D = "q8_d"  # Русское комьюнити

# Question 9
CB_Q9_A = "q9_a"  # Нет детей
CB_Q9_B = "q9_b"  # Малыши
CB_Q9_C = "q9_c"  # Школьники
CB_Q9_D = "q9_d"  # Взрослые

# Question 10
CB_Q10_A = "q10_a"  # Счастлива
CB_Q10_B = "q10_b"  # Несчастлива
CB_Q10_C = "q10_c"  # После расставания
CB_Q10_D = "q10_d"  # Свободна

# Question 11
CB_Q11_A = "q11_a"  # Абсолютно готова
CB_Q11_B = "q11_b"  # Скорее да
CB_Q11_C = "q11_c"  # Хочу, но не уверена
CB_Q11_D = "q11_d"  # Просто изучаю

# Question 12
CB_Q12_A = "q12_a"  # Свободы
CB_Q12_B = "q12_b"  # Найти себя
CB_Q12_C = "q12_c"  # Стабильности
CB_Q12_D = "q12_d"  # Приключений

# Results callbacks
CB_SHOW_RESULT = "show_result"
CB_DOWNLOAD_GUIDE = "download_guide"
CB_FREE_CONSULTATION = "free_consultation"
CB_PAID_CONSULTATION_500 = "paid_consultation_500"
CB_SUBSCRIBE_CHANNEL = "subscribe_channel"


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard with quiz start"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🚀 Пройти тест", callback_data=CB_START_QUIZ)
    )
    builder.row(
        InlineKeyboardButton(text="📖 Узнать больше обо мне", callback_data=CB_ABOUT_ME)
    )
    return builder.as_markup()


def get_story_keyboard() -> InlineKeyboardMarkup:
    """Keyboard after full story"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🚀 Пройти тест", callback_data=CB_START_QUIZ)
    )
    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data=CB_BACK_FROM_STORY)
    )
    return builder.as_markup()


def get_question_1_keyboard() -> InlineKeyboardMarkup:
    """Question 1: What worries you most"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💔 Отношения, которые тянут вниз", callback_data=CB_Q1_A)
    )
    builder.row(
        InlineKeyboardButton(text="💼 Работа без перспектив", callback_data=CB_Q1_B)
    )
    builder.row(
        InlineKeyboardButton(text="😔 Чувство, что жизнь проходит мимо", callback_data=CB_Q1_C)
    )
    builder.row(
        InlineKeyboardButton(text="💸 Финансовая нестабильность", callback_data=CB_Q1_D)
    )
    return builder.as_markup()


def get_question_2_keyboard() -> InlineKeyboardMarkup:
    """Question 2: How long thinking about changes"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📅 Несколько недель", callback_data=CB_Q2_A)
    )
    builder.row(
        InlineKeyboardButton(text="🗓️ Несколько месяцев", callback_data=CB_Q2_B)
    )
    builder.row(
        InlineKeyboardButton(text="📆 Больше года", callback_data=CB_Q2_C)
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Это постоянная мысль", callback_data=CB_Q2_D)
    )
    return builder.as_markup()


def get_question_3_keyboard() -> InlineKeyboardMarkup:
    """Question 3: What stops you"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="😰 Страх неизвестности", callback_data=CB_Q3_A)
    )
    builder.row(
        InlineKeyboardButton(text="💰 Нет денег", callback_data=CB_Q3_B)
    )
    builder.row(
        InlineKeyboardButton(text="👨‍👩‍👧 Мнение близких", callback_data=CB_Q3_C)
    )
    builder.row(
        InlineKeyboardButton(text="🤷‍♀️ Не знаю с чего начать", callback_data=CB_Q3_D)
    )
    return builder.as_markup()


def get_question_4_keyboard() -> InlineKeyboardMarkup:
    """Question 4: Passport"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да, готов", callback_data=CB_Q4_A)
    )
    builder.row(
        InlineKeyboardButton(text="⏰ Да, но скоро истечёт", callback_data=CB_Q4_B)
    )
    builder.row(
        InlineKeyboardButton(text="📋 Нет, но планирую сделать", callback_data=CB_Q4_C)
    )
    builder.row(
        InlineKeyboardButton(text="❌ Нет, не думала об этом", callback_data=CB_Q4_D)
    )
    return builder.as_markup()


def get_question_5_keyboard() -> InlineKeyboardMarkup:
    """Question 5: English level"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎓 Свободно говорю", callback_data=CB_Q5_A)
    )
    builder.row(
        InlineKeyboardButton(text="📚 Базовый (могу объясниться)", callback_data=CB_Q5_B)
    )
    builder.row(
        InlineKeyboardButton(text="📖 Учу сейчас", callback_data=CB_Q5_C)
    )
    builder.row(
        InlineKeyboardButton(text="🚫 Совсем не знаю", callback_data=CB_Q5_D)
    )
    return builder.as_markup()


def get_question_6_keyboard() -> InlineKeyboardMarkup:
    """Question 6: Budget"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💵 До 100 000 ₽", callback_data=CB_Q6_A)
    )
    builder.row(
        InlineKeyboardButton(text="💰 100-300 000 ₽", callback_data=CB_Q6_B)
    )
    builder.row(
        InlineKeyboardButton(text="💎 300-500 000 ₽", callback_data=CB_Q6_C)
    )
    builder.row(
        InlineKeyboardButton(text="🤑 Больше 500 000 ₽", callback_data=CB_Q6_D)
    )
    return builder.as_markup()


def get_question_7_keyboard() -> InlineKeyboardMarkup:
    """Question 7: Climate"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🌴 Тепло круглый год (тропики)", callback_data=CB_Q7_A)
    )
    builder.row(
        InlineKeyboardButton(text="🍂 4 сезона (Европа)", callback_data=CB_Q7_B)
    )
    builder.row(
        InlineKeyboardButton(text="☀️ Умеренный (мягкая зима)", callback_data=CB_Q7_C)
    )
    builder.row(
        InlineKeyboardButton(text="🤷‍♀️ Мне всё равно", callback_data=CB_Q7_D)
    )
    return builder.as_markup()


def get_question_8_keyboard() -> InlineKeyboardMarkup:
    """Question 8: What's important"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🛡️ Безопасность и стабильность", callback_data=CB_Q8_A)
    )
    builder.row(
        InlineKeyboardButton(text="💼 Возможности для заработка", callback_data=CB_Q8_B)
    )
    builder.row(
        InlineKeyboardButton(text="🏝️ Качество жизни и природа", callback_data=CB_Q8_C)
    )
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русское комьюнити", callback_data=CB_Q8_D)
    )
    return builder.as_markup()


def get_question_9_keyboard() -> InlineKeyboardMarkup:
    """Question 9: Children"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👤 Нет", callback_data=CB_Q9_A)
    )
    builder.row(
        InlineKeyboardButton(text="👶 Да, малыши (до 7 лет)", callback_data=CB_Q9_B)
    )
    builder.row(
        InlineKeyboardButton(text="🎒 Да, школьники", callback_data=CB_Q9_C)
    )
    builder.row(
        InlineKeyboardButton(text="👨‍🎓 Да, уже взрослые", callback_data=CB_Q9_D)
    )
    return builder.as_markup()


def get_question_10_keyboard() -> InlineKeyboardMarkup:
    """Question 10: Relationship status"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❤️ В отношениях (счастлива)", callback_data=CB_Q10_A)
    )
    builder.row(
        InlineKeyboardButton(text="💔 В отношениях (несчастлива)", callback_data=CB_Q10_B)
    )
    builder.row(
        InlineKeyboardButton(text="🔓 После расставания/развода", callback_data=CB_Q10_C)
    )
    builder.row(
        InlineKeyboardButton(text="🦋 Свободна", callback_data=CB_Q10_D)
    )
    return builder.as_markup()


def get_question_11_keyboard() -> InlineKeyboardMarkup:
    """Question 11: Ready to move in 6 months"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔥 Да, абсолютно готова!", callback_data=CB_Q11_A)
    )
    builder.row(
        InlineKeyboardButton(text="✅ Скорее да, чем нет", callback_data=CB_Q11_B)
    )
    builder.row(
        InlineKeyboardButton(text="🤔 Хочу, но не уверена", callback_data=CB_Q11_C)
    )
    builder.row(
        InlineKeyboardButton(text="📚 Пока просто изучаю", callback_data=CB_Q11_D)
    )
    return builder.as_markup()


def get_question_12_keyboard() -> InlineKeyboardMarkup:
    """Question 12: What do you expect"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🕊️ Свободы и новых возможностей", callback_data=CB_Q12_A)
    )
    builder.row(
        InlineKeyboardButton(text="✨ Найти себя заново", callback_data=CB_Q12_B)
    )
    builder.row(
        InlineKeyboardButton(text="🛡️ Стабильности и уверенности", callback_data=CB_Q12_C)
    )
    builder.row(
        InlineKeyboardButton(text="🎢 Приключений и эмоций", callback_data=CB_Q12_D)
    )
    return builder.as_markup()


def get_show_result_keyboard() -> InlineKeyboardMarkup:
    """Button to show quiz result"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Показать мой результат", callback_data=CB_SHOW_RESULT)
    )
    return builder.as_markup()


def get_result_type1_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for Type 1 - Dreamer"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📥 Скачать PDF-гайд", callback_data=CB_DOWNLOAD_GUIDE)
    )
    builder.row(
        InlineKeyboardButton(text="💜 Подписаться на канал", callback_data=CB_SUBSCRIBE_CHANNEL)
    )
    return builder.as_markup()


def get_result_type2_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for Type 2 - Ready to start"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📥 Скачать гайд", callback_data=CB_DOWNLOAD_GUIDE)
    )
    builder.row(
        InlineKeyboardButton(text="🎯 Записаться на разбор", callback_data=CB_FREE_CONSULTATION)
    )
    builder.row(
        InlineKeyboardButton(text="💜 Подписаться", callback_data=CB_SUBSCRIBE_CHANNEL)
    )
    return builder.as_markup()


def get_result_type3_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for Type 3 - Bird in cage"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📥 Скачать гайд", callback_data=CB_DOWNLOAD_GUIDE)
    )
    builder.row(
        InlineKeyboardButton(text="💬 Записаться (500₽)", callback_data=CB_PAID_CONSULTATION_500)
    )
    builder.row(
        InlineKeyboardButton(text="🆓 Бесплатный звонок", callback_data=CB_FREE_CONSULTATION)
    )
    builder.row(
        InlineKeyboardButton(text="💜 В канал", callback_data=CB_SUBSCRIBE_CHANNEL)
    )
    return builder.as_markup()


# Scores mapping for quiz
QUIZ_SCORES = {
    # Question 1
    CB_Q1_A: 1, CB_Q1_B: 2, CB_Q1_C: 3, CB_Q1_D: 2,
    # Question 2
    CB_Q2_A: 1, CB_Q2_B: 2, CB_Q2_C: 3, CB_Q2_D: 4,
    # Question 3
    CB_Q3_A: 2, CB_Q3_B: 3, CB_Q3_C: 2, CB_Q3_D: 1,
    # Question 4
    CB_Q4_A: 4, CB_Q4_B: 3, CB_Q4_C: 2, CB_Q4_D: 1,
    # Question 5
    CB_Q5_A: 4, CB_Q5_B: 3, CB_Q5_C: 2, CB_Q5_D: 1,
    # Question 6
    CB_Q6_A: 1, CB_Q6_B: 2, CB_Q6_C: 3, CB_Q6_D: 4,
    # Question 7
    CB_Q7_A: 3, CB_Q7_B: 2, CB_Q7_C: 2, CB_Q7_D: 1,
    # Question 8
    CB_Q8_A: 2, CB_Q8_B: 3, CB_Q8_C: 3, CB_Q8_D: 1,
    # Question 9
    CB_Q9_A: 4, CB_Q9_B: 2, CB_Q9_C: 1, CB_Q9_D: 3,
    # Question 10
    CB_Q10_A: 2, CB_Q10_B: 3, CB_Q10_C: 4, CB_Q10_D: 3,
    # Question 11
    CB_Q11_A: 4, CB_Q11_B: 3, CB_Q11_C: 2, CB_Q11_D: 1,
    # Question 12
    CB_Q12_A: 3, CB_Q12_B: 4, CB_Q12_C: 2, CB_Q12_D: 3,
}
