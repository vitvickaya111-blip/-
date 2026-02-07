from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards.reply import main_menu
from keyboards.inline import education_menu, workshop_actions
from texts.messages import EDUCATION_INTRO, WORKSHOP_BOT, WORKSHOP_SITE
from database.db import update_user_stage
from config import ADMIN_ID

router = Router()


@router.message(F.text == "🎓 Научиться")
async def education(message: Message):
    """Меню обучения"""
    await message.answer(EDUCATION_INTRO, reply_markup=education_menu())
    await update_user_stage(message.from_user.id, "viewing_education")


# === CALLBACKS ===

@router.callback_query(F.data == "edu_bots")
async def cb_edu_bots(callback: CallbackQuery):
    try:
        await callback.message.edit_text(WORKSHOP_BOT, reply_markup=workshop_actions())
    except TelegramBadRequest:
        pass
    await callback.answer()
    await update_user_stage(callback.from_user.id, "viewing_ws_bots")


@router.callback_query(F.data == "edu_sites")
async def cb_edu_sites(callback: CallbackQuery):
    try:
        await callback.message.edit_text(WORKSHOP_SITE, reply_markup=workshop_actions())
    except TelegramBadRequest:
        pass
    await callback.answer()
    await update_user_stage(callback.from_user.id, "viewing_ws_sites")


@router.callback_query(F.data == "ws_register")
async def cb_ws_register(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "🎉 Благодарю за интерес к воркшопу!\n\n"
            "Я получила вашу заявку и свяжусь "
            "в течение 24 часов, чтобы:\n\n"
            "• Подобрать удобную дату\n"
            "• Ответить на вопросы\n"
            "• Отправить всё необходимое\n\n"
            "Если хотите быстрее — пишите сразу: @bugivugi24\n\n"
            "До скорой встречи! 💜"
        )
    except TelegramBadRequest:
        pass

    await callback.answer("Заявка отправлена! ✨")

    try:
        await callback.message.bot.send_message(
            ADMIN_ID,
            f"🎓 ЗАПИСЬ НА ВОРКШОП!\n\n"
            f"👤 {callback.from_user.first_name}\n"
            f"📱 @{callback.from_user.username}\n"
            f"💰 5 000₽\n\n"
            f"ID: {callback.from_user.id}"
        )
    except Exception:
        pass


@router.callback_query(F.data == "ws_question")
async def cb_ws_question(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "💬 ВОПРОСЫ О ВОРКШОПЕ\n\n"
            "Задавайте!\n\n"
            "Напишите: @bugivugi24\n\n"
            "Частые вопросы:\n"
            "• Нужен опыт? — НЕТ!\n"
            "• Если пропущу? — Будет запись\n"
            "• Рассрочка? — Да\n"
            "• Сертификат? — Да!"
        )
    except TelegramBadRequest:
        pass
    await callback.answer()
    await callback.message.answer("Вернуться:", reply_markup=main_menu())


@router.callback_query(F.data == "ws_back")
async def cb_ws_back(callback: CallbackQuery):
    try:
        await callback.message.edit_text(EDUCATION_INTRO, reply_markup=education_menu())
    except TelegramBadRequest:
        pass
    await callback.answer()
