from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import back_to_menu
from texts.messages import ABOUT_ME

router = Router()


@router.message(F.text == "👤 Обо мне")
async def about(message: Message):
    """Обо мне"""
    await message.answer(
        ABOUT_ME,
        reply_markup=back_to_menu()
    )
