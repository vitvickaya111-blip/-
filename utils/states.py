from aiogram.fsm.state import State, StatesGroup


class ConsultationStates(StatesGroup):
    """Состояния для записи на консультацию"""
    name = State()
    business = State()
    task = State()


class BriefStates(StatesGroup):
    """Состояния для брифа"""
    business = State()
    task = State()
    functional = State()
    payment = State()
    deadline = State()
    budget = State()


class CalculatorStates(StatesGroup):
    """Состояния для калькулятора"""
    hours_per_day = State()
    cost_per_hour = State()
