from aiogram.fsm.state import StatesGroup, State


class QuizStates(StatesGroup):
    """States for quiz (test) flow"""
    question_1 = State()  # Что беспокоит больше всего
    question_2 = State()  # Как давно думаешь о переменах
    question_3 = State()  # Что останавливает
    question_4 = State()  # Загранпаспорт
    question_5 = State()  # Уровень английского
    question_6 = State()  # Бюджет на переезд
    question_7 = State()  # Климат
    question_8 = State()  # Что важнее в новой стране
    question_9 = State()  # Наличие детей
    question_10 = State()  # Статус в отношениях
    question_11 = State()  # Готовность переехать в 6 месяцев
    question_12 = State()  # Чего ждешь от перемен


class ConsultationForm(StatesGroup):
    """States for consultation booking form"""
    waiting_for_name = State()
    waiting_for_situation = State()
    waiting_for_concern = State()
    waiting_for_payment_screenshot = State()


class PurchaseStates(StatesGroup):
    """States for product purchase flow"""
    waiting_for_screenshot = State()

