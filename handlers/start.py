from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_menu, diagnostics_start_keyboard
from texts.messages import MAIN_MENU, DIAGNOSTICS_WELCOME
from database.db import add_user, is_user_new, mark_user_not_new

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()

    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""

    await add_user(user_id=user_id, username=username, first_name=first_name)

    if await is_user_new(user_id):
        await message.answer(
            DIAGNOSTICS_WELCOME,
            reply_markup=diagnostics_start_keyboard()
        )
    else:
        await message.answer(
            MAIN_MENU,
            reply_markup=main_menu()
        )


@router.message(F.text == "◀️ Назад в меню")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    await message.answer(
        MAIN_MENU,
        reply_markup=main_menu()
    )
