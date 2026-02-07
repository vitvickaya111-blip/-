from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import main_menu
from texts.messages import ABOUT_ME
from database.db import update_user_stage

router = Router()


@router.message(F.text == "👤 Обо мне")
async def about(message: Message):
    """Обо мне"""
    await message.answer(ABOUT_ME, reply_markup=main_menu())
    await update_user_stage(message.from_user.id, "viewed_about")
