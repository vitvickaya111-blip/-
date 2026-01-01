"""Quiz handlers"""
import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from infrastructure.database.requests import RequestsRepo
from keyboards.quiz import *
from utils.states import QuizStates


router = Router()

# Quiz texts
QUESTION_TEXTS = {
    1: """Отлично! Начинаем 🎯

ВОПРОС 1 из 12:

Что тебя беспокоит больше всего сейчас?""",

    2: """ВОПРОС 2 из 12:

Как давно ты думаешь о переменах?""",

    3: """ВОПРОС 3 из 12:

Что тебя останавливает больше всего?""",

    4: """ВОПРОС 4 из 12:

У тебя есть действующий загранпаспорт?""",

    5: """ВОПРОС 5 из 12:

Какой у тебя уровень английского?""",

    6: """ВОПРОС 6 из 12:

Сколько ты можешь инвестировать в переезд?""",

    7: """ВОПРОС 7 из 12:

Какой климат тебе ближе?""",

    8: """ВОПРОС 8 из 12:

Что важнее в новой стране?""",

    9: """ВОПРОС 9 из 12:

У тебя есть дети?""",

    10: """ВОПРОС 10 из 12:

Твой статус в отношениях?""",

    11: """ВОПРОС 11 из 12:

Готова ли ты переехать в ближайшие 6 месяцев?""",

    12: """ВОПРОС 12 из 12:

Чего ты ждёшь от перемен больше всего?""",
}

ANALYZING_TEXT = """Отлично! Ты ответила на все вопросы 🎉

Сейчас анализирую твои ответы...

⏳ Одну секунду..."""

ANALYZING_DONE_TEXT = """✅ Готово!

Твой тип готовности определён!"""


# Result texts
RESULT_TYPE1_TEXT = """🌙 ТВОЙ ТИП: МЕЧТАТЕЛЬНИЦА

Ты только начинаешь думать о переменах.
И это НОРМАЛЬНО!

📍 ГДЕ ТЫ СЕЙЧАС:

• У тебя есть мечта, но пока нет плана
• Финансы или документы ещё не готовы
• Много вопросов и неопределённости
• Страхи кажутся больше возможностей

Знаешь что?

ИМЕННО С ЭТОГО Я НАЧИНАЛА! ❤️

Через год после "просто мечты"
я уже жила во Вьетнаме.

🎯 ЧТО ТЕБЕ НУЖНО:

✅ План подготовки на 6-12 месяцев
✅ Финансовая стратегия
✅ Пошаговая инструкция с чего начать
✅ Поддержка тех, кто уже прошёл этот путь

🎁 ТВОЙ ПОДАРОК:

Я подготовила для тебя PDF-гайд:

📕 "Вьетнам с ребёнком за 70 000₽"

Мой личный опыт выживания.

Внутри:
• Реальный бюджет по копейкам
• Все сайты для жилья, нянь, врачей
• Контакты и лайфхаки
• План первых 30 дней

А ещё приглашаю в канал "https://t.me/ambasadorsvobody".

Там я делюсь:
✨ Реальными историями переезда
💰 Лайфхаками по визам
🗺️ Обзорами стран
🤗 Поддержкой и мотивацией

Нас уже 37, и растём каждый день!

До встречи! ❤️
Настя"""


RESULT_TYPE2_TEXT = """🚀 ТВОЙ ТИП: ГОТОВАЯ К СТАРТУ

Ого! Ты уже ПОЧТИ готова! 🔥

📍 ГДЕ ТЫ СЕЙЧАС:

• Есть финансы или план накопить
• Загранпаспорт готов (или почти)
• Активно изучаешь информацию
• Но не хватает СИСТЕМЫ

Знаешь, что самое сложное сейчас?

НЕ ПОТЕРЯТЬСЯ В ОКЕАНЕ ИНФОРМАЦИИ.

Я провела 3 месяца в гугле, прежде
чем купила билет.

Половина времени — зря.

Потому что я не знала ЧТО именно нужно.

🎯 ЧТО ТЕБЕ НУЖНО:

✅ Выбрать конкретную страну
✅ Пошаговый план оформления визы
✅ Список районов и цены на жильё
✅ Стратегия первых 30 дней

🌍 СТРАНЫ, КОТОРЫЕ ПОДОЙДУТ:

Исходя из твоих ответов:

🇻🇳 ВЬЕТНАМ — где я выживала
• 70 000₽/мес на двоих
• Лёгкая виза
• Русское комьюнити
• Море и тепло

🇹🇭 ТАИЛАНД — для начинающих
• 80-100 000₽/мес
• Много экспатов
• Инфраструктура

🇬🇪 ГРУЗИЯ — близко к дому
• 80-120 000₽/мес
• Год без визы
• Русский язык

🇧🇷 БРАЗИЛИЯ — где я сейчас
• 100-150 000₽/мес
• Лёгкая виза
• Тепло и свобода

🎁 ТВОЙ ПОДАРОК:

📕 PDF-гайд "Вьетнам за 70 000₽"

Мой опыт выживания с грудным ребёнком.

Внутри ВСЁ:
• Реальный бюджет
• Сайты для жилья, нянь, врачей
• Контакты
• План первых 30 дней

💬 БОНУС ДЛЯ ТЕБЯ:

Ты почти готова, поэтому предлагаю:

БЕСПЛАТНЫЙ 15-МИНУТНЫЙ РАЗБОР

Быстро обсудим твою ситуацию
и я дам конкретные шаги.

Но сначала подпишись на канал —
там делюсь обновлениями.

До встречи! 💪
Настя"""


RESULT_TYPE3_TEXT = """🦅 ТВОЙ ТИП: ПТИЦА В КЛЕТКЕ

Господи, как же я тебя понимаю! 😭

📍 ГДЕ ТЫ СЕЙЧАС:

• У тебя УЖЕ есть ВСЁ: деньги, документы, желание
• Готова улететь хоть завтра
• Но что-то держит
• Этот конфликт разрывает изнутри

Знаешь что это?

СТРАХ.

Не страх бедности.
А страх ПРИНЯТЬ РЕШЕНИЕ.

Потому что решение = точка невозврата.

Ты боишься:
❌ Пожалеешь
❌ Не справишься
❌ Разочаруешься
❌ Потеряешь то, что есть

Я провела в этом состоянии 4 месяца.

Смотрела на билет в корзине
и не могла нажать "купить".

Знаешь что помогло?

ПОДДЕРЖКА.

Девочка из инстаграма сказала:

"Настя, даже если не понравится —
ты ВСЕГДА можешь вернуться.
Это не тюрьма. Это эксперимент."

Я купила билет в тот же вечер.

🎯 ЧТО ТЕБЕ НУЖНО:

✅ НЕ информация (её у тебя много)
✅ А ПОДДЕРЖКА и структура
✅ Кто-то скажет: "Давай, справишься"
✅ И будет рядом, когда станет страшно

🎁 ТВОЙ ПОДАРОК:

📕 Гайд "Вьетнам с ребёнком за 70к"

Хотя ты, возможно, выберешь другую страну.

Но в гайде есть моя история выживания.
Может, она вдохновит.

💬 СПЕЦИАЛЬНО ДЛЯ ТЕБЯ:

Таким как ты нужна НЕ информация.

Нужна ПОДДЕРЖКА.

Поэтому предлагаю:

КОНСУЛЬТАЦИЯ 30 МИНУТ (500₽)

Обсудим:
✓ Что конкретно тебя держит
✓ Как преодолеть страх
✓ Конкретные шаги на эту неделю
✓ Я буду на связи после

Или просто ПОГОВОРИМ бесплатно 10 минут.

И обязательно в канал — там девочки
в похожей ситуации.

Я верю в тебя.
Ты УЖЕ готова.
Осталось сделать шаг.

❤️ Настя"""


@router.callback_query(F.data == CB_START_QUIZ)
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """Start quiz"""
    await state.clear()
    await state.update_data(total_score=0)
    await state.set_state(QuizStates.question_1)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[1],
        reply_markup=get_question_1_keyboard()
    )
    await callback.answer()


# Question 1 handlers
@router.callback_query(QuizStates.question_1)
async def process_question_1(callback: CallbackQuery, state: FSMContext):
    """Process question 1 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_2)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[2],
        reply_markup=get_question_2_keyboard()
    )
    await callback.answer()


# Question 2 handlers
@router.callback_query(QuizStates.question_2)
async def process_question_2(callback: CallbackQuery, state: FSMContext):
    """Process question 2 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_3)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[3],
        reply_markup=get_question_3_keyboard()
    )
    await callback.answer()


# Question 3 handlers
@router.callback_query(QuizStates.question_3)
async def process_question_3(callback: CallbackQuery, state: FSMContext):
    """Process question 3 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_4)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[4],
        reply_markup=get_question_4_keyboard()
    )
    await callback.answer()


# Question 4 handlers
@router.callback_query(QuizStates.question_4)
async def process_question_4(callback: CallbackQuery, state: FSMContext):
    """Process question 4 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_5)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[5],
        reply_markup=get_question_5_keyboard()
    )
    await callback.answer()


# Question 5 handlers
@router.callback_query(QuizStates.question_5)
async def process_question_5(callback: CallbackQuery, state: FSMContext):
    """Process question 5 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_6)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[6],
        reply_markup=get_question_6_keyboard()
    )
    await callback.answer()


# Question 6 handlers
@router.callback_query(QuizStates.question_6)
async def process_question_6(callback: CallbackQuery, state: FSMContext):
    """Process question 6 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_7)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[7],
        reply_markup=get_question_7_keyboard()
    )
    await callback.answer()


# Question 7 handlers
@router.callback_query(QuizStates.question_7)
async def process_question_7(callback: CallbackQuery, state: FSMContext):
    """Process question 7 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_8)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[8],
        reply_markup=get_question_8_keyboard()
    )
    await callback.answer()


# Question 8 handlers
@router.callback_query(QuizStates.question_8)
async def process_question_8(callback: CallbackQuery, state: FSMContext):
    """Process question 8 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_9)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[9],
        reply_markup=get_question_9_keyboard()
    )
    await callback.answer()


# Question 9 handlers
@router.callback_query(QuizStates.question_9)
async def process_question_9(callback: CallbackQuery, state: FSMContext):
    """Process question 9 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_10)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[10],
        reply_markup=get_question_10_keyboard()
    )
    await callback.answer()


# Question 10 handlers
@router.callback_query(QuizStates.question_10)
async def process_question_10(callback: CallbackQuery, state: FSMContext):
    """Process question 10 answer"""
    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score
    
    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_11)
    
    await callback.message.edit_text(
        QUESTION_TEXTS[11],
        reply_markup=get_question_11_keyboard()
    )
    await callback.answer()


# Question 11 handlers
@router.callback_query(QuizStates.question_11)
async def process_question_11(callback: CallbackQuery, state: FSMContext):
    """Process question 11 answer"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Question 11 handler triggered with callback_data: {callback.data}")

    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score

    await state.update_data(total_score=total_score)
    await state.set_state(QuizStates.question_12)

    logger.info(f"Question 11 processed. Total score: {total_score}. State set to question_12")

    await callback.message.edit_text(
        QUESTION_TEXTS[12],
        reply_markup=get_question_12_keyboard()
    )
    await callback.answer()


# Question 12 handlers (last question)
@router.callback_query(QuizStates.question_12)
async def process_question_12(callback: CallbackQuery, state: FSMContext):
    """Process question 12 answer and show analyzing message"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Question 12 handler triggered with callback_data: {callback.data}")

    score = QUIZ_SCORES.get(callback.data, 0)
    data = await state.get_data()
    total_score = data.get('total_score', 0) + score

    logger.info(f"Question 12: score={score}, total_score={total_score}")

    # Store final score before clearing state
    await state.update_data(final_score=total_score)
    await state.clear()

    # Set data again after clear
    await state.update_data(final_score=total_score)

    await callback.message.edit_text(ANALYZING_TEXT, reply_markup=None)
    await callback.answer()

    logger.info("Waiting 3 seconds before showing result button...")
    # Wait 3 seconds
    await asyncio.sleep(3)

    await callback.message.edit_text(
        ANALYZING_DONE_TEXT,
        reply_markup=get_show_result_keyboard()
    )
    logger.info("Question 12 handler completed")


@router.callback_query(F.data == CB_SHOW_RESULT)
async def show_result(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    """Show quiz result based on score"""
    data = await state.get_data()
    score = data.get('final_score', 0)
    
    # Mark quiz as completed
    await repo.users.update(
        callback.from_user.id,
        downloaded_pdf=False,  # Will be set to True when they download
        autoresponder_day=0
    )
    
    # Determine result type
    # 0-15 = Type 1, 16-28 = Type 2, 29-48 = Type 3
    if score <= 15:
        result_text = RESULT_TYPE1_TEXT
        keyboard = get_result_type1_keyboard()
    elif score <= 28:
        result_text = RESULT_TYPE2_TEXT
        keyboard = get_result_type2_keyboard()
    else:
        result_text = RESULT_TYPE3_TEXT
        keyboard = get_result_type3_keyboard()
    
    await callback.message.edit_text(result_text, reply_markup=keyboard)
    await callback.answer()
    
    # Send Day 0 message after showing result
    from services.auto_funnel import send_day_0_message_quiz
    await send_day_0_message_quiz(callback.bot, callback.from_user.id)
