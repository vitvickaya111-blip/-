from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.reply import education_menu, main_menu
from keyboards.inline import (
    get_education_buttons, get_workshop_list,
    get_workshop_actions
)
from texts.messages import EDUCATION_INTRO, WORKSHOP_4H
from database.db import update_user_stage
from config import ADMIN_ID

router = Router()


@router.message(F.text == "🎓 Научиться")
async def education(message: Message):
    """Меню обучения"""
    await message.answer(EDUCATION_INTRO, reply_markup=get_education_buttons())
    await message.answer("👇 Или внизу:", reply_markup=education_menu())
    await update_user_stage(message.from_user.id, "viewing_education")


@router.message(F.text == "🤖 Воркшопы по ботам")
async def edu_bots(message: Message):
    await message.answer("🤖 ВОРКШОПЫ ПО БОТАМ\n\nВыберите формат:", reply_markup=get_workshop_list())


# --- Callbacks ---

@router.callback_query(F.data == "edu_bots")
async def cb_edu_bots(callback: CallbackQuery):
    await callback.message.edit_text(
        "🤖 ВОРКШОПЫ ПО БОТАМ\n\nВыберите формат:", reply_markup=get_workshop_list()
    )
    await callback.answer()


@router.callback_query(F.data == "ws_4h")
async def cb_ws_4h(callback: CallbackQuery):
    await callback.message.edit_text(WORKSHOP_4H, reply_markup=get_workshop_actions())
    await callback.answer()
    await update_user_stage(callback.from_user.id, "viewing_ws_4h")


@router.callback_query(F.data == "register_workshop")
async def cb_register(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ СУПЕР!\n\n"
        "Формат: Суббота | 10:00-14:00 (МСК) | Онлайн (Zoom)\n"
        "Стоимость: 5 000₽\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎁 БОНУС СЕГОДНЯ:\n"
        "Воркшоп по деплою БЕСПЛАТНО!\n"
        "(экономите 3 000₽)\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📝 СЛЕДУЮЩИЙ ШАГ:\n\n"
        "Напишите: @bugivugi24\n\n"
        "Пришлю:\n"
        "• Подберём удобную дату\n"
        "• Реквизиты\n"
        "• Ссылку на Zoom\n"
        "• Материалы\n\n"
        "До встречи! 🚀"
    )

    await callback.answer("Записываемся! 🚀")

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

    await callback.message.answer("Что дальше?", reply_markup=main_menu())


@router.callback_query(F.data == "ask_workshop_q")
async def cb_ask_ws_q(callback: CallbackQuery):
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
    await callback.answer()
    await callback.message.answer("Вернуться:", reply_markup=main_menu())


@router.callback_query(F.data == "back_to_workshops")
async def cb_back_workshops(callback: CallbackQuery):
    await callback.message.edit_text(
        "🤖 ВОРКШОПЫ ПО БОТАМ\n\nВыберите:", reply_markup=get_workshop_list()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_education")
async def cb_back_education(callback: CallbackQuery):
    await callback.message.edit_text(EDUCATION_INTRO, reply_markup=get_education_buttons())
    await callback.answer()


@router.callback_query(F.data.in_({"edu_sites", "edu_autopost", "edu_ai",
                                    "ws_weekend", "ws_intensive", "ws_combo"}))
async def cb_other_edu(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Этот раздел скоро! 🔜\n\nХотите обсудить?\nПишите: @bugivugi24"
    )
    await callback.answer("Скоро! 🚀")
    await callback.message.answer("Вернуться:", reply_markup=main_menu())


@router.message(F.text.in_(["🌐 Воркшопы по сайтам", "🧠 AI-инструменты"]))
async def other_edu(message: Message):
    await message.answer(
        f"Раздел '{message.text}' скоро!\n\nНапишите: @bugivugi24",
        reply_markup=education_menu()
    )
