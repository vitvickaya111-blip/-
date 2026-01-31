from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import education_menu, education_bots_menu
from texts.messages import EDUCATION_MENU, WORKSHOP_4H

router = Router()


@router.message(F.text == "🎓 Научиться самому")
async def education(message: Message):
    """Меню обучения"""
    await message.answer(
        EDUCATION_MENU,
        reply_markup=education_menu()
    )


@router.message(F.text == "🤖 Создание Telegram-ботов")
async def education_bots(message: Message):
    """Обучение созданию ботов"""
    await message.answer(
        "🤖 ОБУЧЕНИЕ: СОЗДАНИЕ TELEGRAM-БОТОВ\n\n"
        "Научу делать ботов с помощью Claude AI + Python + Cursor\n"
        "БЕЗ глубоких знаний программирования!",
        reply_markup=education_bots_menu()
    )


@router.message(F.text == "◀️ Назад к обучению")
async def back_to_education(message: Message):
    """Назад к обучению"""
    await message.answer(
        EDUCATION_MENU,
        reply_markup=education_menu()
    )


@router.message(F.text == "⚡ Первый бот за 4 часа - 5 000₽")
async def workshop_4h_info(message: Message):
    """Информация о воркшопе 4 часа"""
    await message.answer(WORKSHOP_4H, reply_markup=education_bots_menu())


@router.message(F.text.in_([
    "📱 Бот-визитка - 7 000₽",
    "🚀 Интенсив 7 дней - 15 000₽",
    "📖 Воркшоп по деплою - 3 000₽",
    "💎 Комбо-пакет - 35 000₽"
]))
async def other_bot_workshops(message: Message):
    """Остальные воркшопы по ботам (заглушка)"""
    await message.answer(
        f"Подробное описание '{message.text}' скоро появится.\n\n"
        f"Хотите записаться?\n"
        f"Напишите мне: @nastya",
        reply_markup=education_bots_menu()
    )


@router.message(F.text.in_([
    "🌐 Создание сайтов с AI",
    "📊 Автопостинг и автоматизация",
    "🧠 Работа с AI"
]))
async def other_education(message: Message):
    """Остальные направления обучения (заглушка)"""
    await message.answer(
        f"Раздел '{message.text}' скоро появится.\n\n"
        f"Хотите узнать подробнее?\n"
        f"Напишите мне: @nastya",
        reply_markup=education_menu()
    )
