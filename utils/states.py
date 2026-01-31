from aiogram.fsm.state import State, StatesGroup


class ConsultationStates(StatesGroup):
    """Состояния для записи на консультацию"""
    name = State()
    business = State()
    task = State()


class BriefBotStates(StatesGroup):
    """Состояния для брифа на бота"""
    business = State()
    task = State()
    functional = State()
    payment = State()
    deadline = State()
    budget = State()


class DiagnosticsStates(StatesGroup):
    """Состояния для диагностики (воронка)"""
    business = State()
    automation = State()
    budget = State()
