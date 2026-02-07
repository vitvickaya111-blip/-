from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import CalculatorStates
from texts.messages import CALC_INTRO, CALC_ASK_HOURS, CALC_ASK_COST, get_calc_result
from keyboards.reply import main_menu, cancel_kb
from keyboards.inline import calc_actions
from database.db import save_calculation, get_user

router = Router()


@router.message(F.text == "🧮 Калькулятор")
async def calculator_start(message: Message, state: FSMContext):
    """Запуск калькулятора"""
    await state.set_state(CalculatorStates.hours_per_day)
    await message.answer(
        CALC_INTRO + "\n\n" + CALC_ASK_HOURS,
        reply_markup=cancel_kb()
    )


@router.message(CalculatorStates.hours_per_day)
async def process_hours(message: Message, state: FSMContext):
    """Обработка часов"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    try:
        hours = float(message.text.replace(',', '.'))
        if hours <= 0 or hours > 24:
            await message.answer(
                "🤔 Введите реальное число часов (от 0.5 до 24)\n\n" +
                CALC_ASK_HOURS
            )
            return

        await state.update_data(hours=hours)
        await state.set_state(CalculatorStates.cost_per_hour)
        await message.answer(CALC_ASK_COST, reply_markup=cancel_kb())

    except ValueError:
        await message.answer(
            "❌ Не понял... Введите просто число.\n"
            "Например: 3.5\n\n" + CALC_ASK_HOURS
        )


@router.message(CalculatorStates.cost_per_hour)
async def process_cost(message: Message, state: FSMContext):
    """Обработка стоимости"""
    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("Отменено.", reply_markup=main_menu())
        return

    try:
        cost = float(message.text.replace(',', '.').replace('₽', '').replace(' ', ''))
        if cost <= 0:
            await message.answer(
                "🤔 Введите реальную стоимость (больше 0)\n\n" + CALC_ASK_COST
            )
            return

        data = await state.get_data()
        hours = data['hours']

        user = await get_user(message.from_user.id)
        first_name = user['first_name'] if user else message.from_user.first_name or "друг"

        hours_per_month = hours * 30
        loss_per_month = hours_per_month * cost
        loss_per_year = loss_per_month * 12

        await save_calculation(
            user_id=message.from_user.id,
            hours=hours,
            cost=cost,
            monthly_loss=loss_per_month,
            yearly_loss=loss_per_year
        )

        result = get_calc_result(first_name, hours, cost)

        await message.answer(result, reply_markup=calc_actions())
        await message.answer("Что делаем дальше?", reply_markup=main_menu())

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Не понял... Введите просто число.\n"
            "Например: 2000\n\n" + CALC_ASK_COST
        )
