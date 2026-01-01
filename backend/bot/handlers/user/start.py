from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from infrastructure.database.requests import RequestsRepo
from keyboards.inline import (
    get_after_guide_keyboard, get_back_to_menu_keyboard,
    get_consultation_keyboard, get_situation_keyboard, get_concern_keyboard,
    get_payment_keyboard, get_payment_confirmation_keyboard,
    get_auto_funnel_day7_keyboard,
    CB_GET_GUIDE, CB_CONSULTATION, CB_BACK_TO_MENU,
    CB_BOOK_CONSULTATION, CB_ASK_QUESTION, CB_PAY_CONSULTATION, CB_PAID_SCREENSHOT,
    CB_SITUATION_TOXIC, CB_SITUATION_SINGLE_MOM, CB_SITUATION_BURNOUT,
    CB_SITUATION_WANT_RELOCATE, CB_SITUATION_CUSTOM,
    CB_CONCERN_FINANCES, CB_CONCERN_FEARS, CB_CONCERN_DONT_KNOW,
    CB_CONCERN_FAMILY, CB_CONCERN_CUSTOM, CB_FUNNEL_YES, CB_FUNNEL_NO
)
from keyboards.quiz import (
    get_start_keyboard, get_story_keyboard,
    CB_ABOUT_ME, CB_BACK_FROM_STORY, CB_DOWNLOAD_GUIDE, CB_SUBSCRIBE_CHANNEL,
    CB_FREE_CONSULTATION, CB_PAID_CONSULTATION_500
)
from utils.states import ConsultationForm

router = Router()

# Texts from instructions
WELCOME_TEXT = """Привет! Я Настя 👋

8 лет я была старшим лейтенантом ФСИН.
Работала в колонии строгого режима.

Потом я сбежала.

Не из страны — из СИСТЕМЫ.

Я прошла через:
💔 Развод с наркоманом
👶 Роды в Бразилии с $1000 в кармане
😔 Абьюз в России
✈️ Побег во Вьетнам с грудным ребёнком

Но я выжила.

Сейчас в Бразилии. Счастлива.
Помогаю другим женщинам вырваться из клетки.

У меня для тебя есть тест:

🎯 "ГОТОВА ЛИ ТЫ К ПЕРЕМЕНАМ?"

Он покажет:
✅ На каком этапе ты сейчас
✅ Что тебя останавливает
✅ Какие шаги делать дальше

Займёт 3 минуты.

В конце получишь персональный результат
+ подарок 🎁"""

GUIDE_TEXT = """🎁 ГАЙД "КАК Я ВЫЖИЛА ВО ВЬЕТНАМЕ"

Это мой личный опыт выживания с грудным ребёнком на 70 000₽/месяц.

Внутри ты найдёшь:
✅ Мой реальный бюджет (по копейкам)
✅ Все сайты для поиска жилья
✅ Контакты врачей, нянь, магазинов
✅ Пошаговый план первых 30 дней
✅ Лайфхаки для мам-одиночек

📥 Скачать гайд:
[Здесь будет ссылка на файл или отправка файла]

После скачивания обязательно подпишись на мой канал "Женщины в движении" — там я делюсь обновлениями, историями других девочек и отвечаю на вопросы:

P.S. Если у тебя есть вопросы — просто напиши мне здесь, я отвечу! ❤️"""

FULL_STORY_TEXT = """📖 МОЯ ПОЛНАЯ ИСТОРИЯ

Я родилась в обычной семье.
Мама умерла от рака в 2012 году.

8 лет работала в ФСИН. Инспектор
в колонии строгого режима.
Старший лейтенант.

Стабильность. Зарплата. Погоны.

Но внутри задыхалась.

Встретила мужчину: "Давай уедем".
Уволилась.

Путешествовали по Азии. Забеременела.
Родила в Бразилии.

Потом всё рухнуло.

Наркотики. Насилие.

Улетела в Россию с грудным сыном.
$3000 в кармане. $2000 — на билеты.

В России — абьюз. Мамы нет.
Некуда идти.

Заняла у подруги. Купила билет во Вьетнам.
$1000 и ребёнок на руках.

Не знала языка. Не было связей.

Первые месяцы — ад.

Но справилась.

Сейчас в Бразилии. Новый партнёр
(на 9 лет младше). Ребёнок счастлив.

Алименты 7000₽, хотя бывший живёт богато.

Но мне не нужна его помощь.

Я СВОБОДНА.

Если я смогла — сможешь и ты."""

CONSULTATION_TEXT = """💬 КОНСУЛЬТАЦИЯ СО МНОЙ

Я провожу личные консультации для женщин, которые:
• Хотят переехать, но не знают с чего начать
• В сложной ситуации и нужна поддержка
• Хотят разобрать свой конкретный случай

⏰ Формат: 30 минут по видеосвязи (Zoom/WhatsApp)

💰 Стоимость: 500₽

Что будет на консультации:
✓ Разберём твою ситуацию (финансы, дети, документы)
✓ Подберём страну под твой бюджет
✓ Составим план первых шагов
✓ Я отвечу на ВСЕ твои вопросы
✓ Дам контакты и лайфхаки

Это НЕ продажа курсов. Это реальная помощь от женщины, которая прошла через это."""


@router.message(CommandStart())
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo):
    await state.clear()

    # User already created in middleware
    await message.answer(WELCOME_TEXT, reply_markup=get_start_keyboard())


@router.callback_query(F.data == CB_ABOUT_ME)
async def about_me_handler(callback: CallbackQuery):
    """Show full story"""
    await callback.message.edit_text(FULL_STORY_TEXT, reply_markup=get_story_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_BACK_FROM_STORY)
async def back_from_story_handler(callback: CallbackQuery):
    """Go back to main menu from story"""
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=get_start_keyboard())
    await callback.answer()


@router.message(Command("help"))
async def help_command(message: Message):
    help_text = """🆘 ПОМОЩЬ И НАВИГАЦИЯ

Что я могу сделать:

🎁 /start — Вернуться в главное меню
📥 Скачать гайд по Вьетнаму
💬 Записаться на консультацию (500₽)
📢 Подписаться на мой канал "Амбасадор свободы"

❓ Есть вопрос? Просто напиши мне — я отвечу!

💌 Или пиши напрямую в Instagram: @podruga_iz_brazilii"""

    await message.answer(help_text, reply_markup=get_back_to_menu_keyboard())


@router.message(Command("channel"))
async def channel_command(message: Message):
    channel_text = """📢 МОЙ TELEGRAM-КАНАЛ

Амбасадор свободы

Подписывайся, там я делюсь:
• Историями других девочек
• Обновлениями из Бразилии
• Советами по переезду
• Отвечаю на вопросы подписчиц

https://t.me/ambasadorsvobody"""

    await message.answer(channel_text, reply_markup=get_back_to_menu_keyboard())


@router.message(Command("consultation"))
async def consultation_command(message: Message):
    await message.answer(CONSULTATION_TEXT, reply_markup=get_consultation_keyboard())


# Callback handlers
@router.callback_query(F.data == CB_BACK_TO_MENU)
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=get_start_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_DOWNLOAD_GUIDE)
async def download_guide_handler(callback: CallbackQuery, repo: RequestsRepo):
    """Handle PDF guide download from quiz results"""
    # Mark user as downloaded PDF
    await repo.users.update(
        callback.from_user.id,
        downloaded_pdf=True,
        autoresponder_day=0
    )

    await callback.answer("📥 Отправляю гайд...", show_alert=False)

    # Send PDF file from URL
    from aiogram.utils.markdown import hlink

    pdf_url = "https://pdfhost.io/v/Sf7YZvWQga_vietnam"

    try:
        await callback.message.answer(f"📕 Вот твой PDF-гайд {hlink("Вьетнам с ребёнком за 70 000₽", pdf_url)}\"\n\n"
                    f"Скачивай и изучай! 💜")
    except Exception as e:
        # If sending by URL fails, send direct link
        await callback.message.answer(
            "📕 PDF-гайд \"Вьетнам с ребёнком за 70 000₽\"\n\n"
            "📥 Скачать гайд: https://pdfhost.io/v/Sf7YZvWQga_vietnam\n\n"
            "Или напиши мне, и я отправлю его тебе лично! 💜"
        )


@router.callback_query(F.data == CB_SUBSCRIBE_CHANNEL)
async def subscribe_channel_handler(callback: CallbackQuery):
    """Send channel link"""
    channel_text = """📢 ПОДПИСЫВАЙСЯ НА КАНАЛ

Амбасадор свободы

Там я делюсь:
✨ Реальными историями переезда
💰 Лайфхаками по визам
🗺️ Обзорами стран
🤗 Поддержкой и мотивацией

@ambasadorsvobody

Жду тебя! 💜"""

    await callback.message.answer(channel_text)
    await callback.answer()


@router.callback_query(F.data == CB_FREE_CONSULTATION)
async def free_consultation_handler(callback: CallbackQuery):
    """Handle free consultation request"""
    # Logging
    print(f"🔔 Нажата кнопка бесплатного звонка пользователем {callback.from_user.id} (@{callback.from_user.username or 'нет username'})")

    await callback.answer("Записываю тебя на бесплатный звонок!", show_alert=True)

    await callback.message.answer(
        "📞 Отлично! Запишу тебя на бесплатный 10-минутный звонок.\n\n"
        "Напиши мне:\n"
        "• Удобное время для звонка\n"
        "• Твой часовой пояс\n\n"
        "Я свяжусь с тобой в ближайшее время! 💜"
    )

    # Notify admin
    admin_id = 255724496
    try:
        username_info = f"@{callback.from_user.username}" if callback.from_user.username else f"ID: {callback.from_user.id}"
        contact_link = f"tg://user?id={callback.from_user.id}"

        notification_text = (
            "📞 Новая заявка на БЕСПЛАТНУЮ консультацию!\n\n"
            f"👤 Имя: {callback.from_user.first_name}\n"
            f"📱 Username: {username_info}\n\n"
            f"Связаться с клиентом: {contact_link}"
        )

        await callback.bot.send_message(admin_id, notification_text)
        print(f"✅ Уведомление админу отправлено успешно")
    except Exception as e:
        print(f"❌ Ошибка отправки уведомления админу: {e}")


@router.callback_query(F.data == CB_PAID_CONSULTATION_500)
async def paid_consultation_handler(callback: CallbackQuery, state: FSMContext):
    """Start paid consultation booking"""
    await callback.answer()
    await callback.message.answer(
        "Отлично! Начнём запись на консультацию.\n\n"
        "1️⃣ Как тебя зовут?\n(Напиши своё имя)",
        reply_markup=None
    )
    await state.set_state(ConsultationForm.waiting_for_name)


@router.callback_query(F.data == CB_GET_GUIDE)
async def get_guide_handler(callback: CallbackQuery, repo: RequestsRepo):
    # Mark user as downloaded PDF and set autoresponder_day to 0
    await repo.users.update(
        callback.from_user.id,
        downloaded_pdf=True,
        autoresponder_day=0
    )

    await callback.message.edit_text(GUIDE_TEXT, reply_markup=get_after_guide_keyboard())
    await callback.answer()

    # Send PDF file from URL
    pdf_url = "https://pdfhost.io/v/Sf7YZvWQga_vietnam"

    try:
        pdf_file = URLInputFile(pdf_url, filename="vietnam_guide.pdf")
        await callback.message.answer_document(
            pdf_file,
            caption="📥 Вот твой гайд! Скачивай и изучай 💜"
        )
    except Exception:
        pass  # Silently fail, user got the text message anyway

    # Send Day 0 message from auto-funnel
    from services.auto_funnel import send_day_0_message
    await send_day_0_message(callback.bot, callback.from_user.id)


@router.callback_query(F.data == CB_CONSULTATION)
async def consultation_handler(callback: CallbackQuery):
    await callback.message.edit_text(CONSULTATION_TEXT, reply_markup=get_consultation_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_ASK_QUESTION)
async def ask_question_handler(callback: CallbackQuery):
    text = """Отлично! Просто напиши мне свой вопрос здесь, и я отвечу в течение 24 часов.

Задавай любой вопрос о консультации, переезде или моём опыте 💌"""

    await callback.message.edit_text(text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_BOOK_CONSULTATION)
async def book_consultation_handler(callback: CallbackQuery, state: FSMContext):
    text = """📝 ЗАПИСЬ НА КОНСУЛЬТАЦИЮ

Для записи мне нужна информация о тебе.

Пожалуйста, ответь на несколько вопросов:

1️⃣ Как тебя зовут?
(Напиши своё имя)"""

    await callback.message.edit_text(text, reply_markup=None)
    await state.set_state(ConsultationForm.waiting_for_name)
    await callback.answer()


# Consultation form handlers
@router.message(ConsultationForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext, repo: RequestsRepo):
    name = message.text
    await state.update_data(name=name)

    # Save to database
    await repo.users.update(
        message.from_user.id,
        consultation_name=name,
        consultation_requested=True
    )

    text = """2️⃣ Какая у тебя ситуация сейчас?

Выбери, что подходит больше всего:"""

    await message.answer(text, reply_markup=get_situation_keyboard())
    await state.set_state(ConsultationForm.waiting_for_situation)


@router.callback_query(ConsultationForm.waiting_for_situation)
async def process_situation(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    situation_map = {
        CB_SITUATION_TOXIC: "💔 В токсичных отношениях",
        CB_SITUATION_SINGLE_MOM: "👶 Мама-одиночка / после развода",
        CB_SITUATION_BURNOUT: "💼 Выгорание на работе / в системе",
        CB_SITUATION_WANT_RELOCATE: "🌍 Просто хочу переехать",
        CB_SITUATION_CUSTOM: "Напишу сама"
    }

    if callback.data == CB_SITUATION_CUSTOM:
        await callback.message.edit_text("Опиши свою ситуацию своими словами:")
        await callback.answer()
        return

    situation = situation_map.get(callback.data, "Другое")
    await state.update_data(situation=situation)

    # Save to database
    await repo.users.update(
        callback.from_user.id,
        consultation_situation=situation
    )

    text = """3️⃣ Что тебя беспокоит больше всего?"""

    await callback.message.edit_text(text, reply_markup=get_concern_keyboard())
    await state.set_state(ConsultationForm.waiting_for_concern)
    await callback.answer()


@router.message(ConsultationForm.waiting_for_situation)
async def process_situation_text(message: Message, state: FSMContext, repo: RequestsRepo):
    situation = message.text
    await state.update_data(situation=situation)

    # Save to database
    await repo.users.update(
        message.from_user.id,
        consultation_situation=situation
    )

    text = """3️⃣ Что тебя беспокоит больше всего?"""

    await message.answer(text, reply_markup=get_concern_keyboard())
    await state.set_state(ConsultationForm.waiting_for_concern)


@router.callback_query(ConsultationForm.waiting_for_concern)
async def process_concern(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    concern_map = {
        CB_CONCERN_FINANCES: "💰 Финансы / нет денег",
        CB_CONCERN_FEARS: "😰 Страхи и неуверенность",
        CB_CONCERN_DONT_KNOW: "📋 Не знаю с чего начать",
        CB_CONCERN_FAMILY: "👨‍👩‍👧 Дети / семья держит",
        CB_CONCERN_CUSTOM: "Напишу сама"
    }

    if callback.data == CB_CONCERN_CUSTOM:
        await callback.message.edit_text("Напиши, что тебя беспокоит больше всего:")
        await callback.answer()
        return

    concern = concern_map.get(callback.data, "Другое")
    await state.update_data(concern=concern)

    # Save to database
    await repo.users.update(
        callback.from_user.id,
        consultation_concern=concern
    )

    data = await state.get_data()
    name = data.get('name', 'дорогая')

    text = f"""Отлично, {name}!

Я уже вижу твою ситуацию и понимаю, как могу помочь.

Консультация стоит 500₽.

После оплаты я свяжусь с тобой в течение 24 часов для согласования времени созвона."""

    await callback.message.edit_text(text, reply_markup=get_payment_keyboard())
    await state.clear()
    await callback.answer()


@router.message(ConsultationForm.waiting_for_concern)
async def process_concern_text(message: Message, state: FSMContext, repo: RequestsRepo):
    concern = message.text
    await state.update_data(concern=concern)

    # Save to database
    await repo.users.update(
        message.from_user.id,
        consultation_concern=concern
    )

    data = await state.get_data()
    name = data.get('name', 'дорогая')

    text = f"""Отлично, {name}!

Я уже вижу твою ситуацию и понимаю, как могу помочь.

Консультация стоит 500₽.

После оплаты я свяжусь с тобой в течение 24 часов для согласования времени созвона."""

    await message.answer(text, reply_markup=get_payment_keyboard())
    await state.clear()


@router.callback_query(F.data == CB_PAY_CONSULTATION)
async def pay_consultation(callback: CallbackQuery, state: FSMContext):
    # TODO: Integrate with payment system (YooKassa/Stripe)
    # For now, show manual payment details

    payment_text = """💳 РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:

Сбербанк: 2202201451883538
Получатель: Анастасия У.

Сумма: 500₽

После оплаты пришли скриншот сюда — я подтвержу и свяжусь с тобой в течение 24 часов для записи!"""

    await callback.message.edit_text(payment_text, reply_markup=get_payment_confirmation_keyboard())
    await state.set_state(ConsultationForm.waiting_for_payment_screenshot)
    await callback.answer()


@router.callback_query(F.data == CB_PAID_SCREENSHOT)
async def paid_screenshot_prompt(callback: CallbackQuery):
    await callback.message.edit_text(
        "Отлично! Пришли, пожалуйста, скриншот оплаты 📸",
        reply_markup=None
    )
    await callback.answer()


@router.message(ConsultationForm.waiting_for_payment_screenshot, F.photo)
async def process_payment_screenshot(message: Message, state: FSMContext, repo: RequestsRepo):
    # Save payment screenshot info
    await repo.users.update(
        message.from_user.id,
        consultation_paid=True
    )

    # Get user data from database
    user = await repo.users.get(message.from_user.id)
    user_name = user.consultation_name if user and user.consultation_name else message.from_user.first_name

    # Notify admin about new payment - send to specific admin ID
    admin_id = 255724496
    try:
        # Prepare admin notification text
        username_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        contact_link = f"tg://user?id={message.from_user.id}"

        notification_text = (
            "🔔 Новая заявка на консультацию!\n\n"
            f"👤 Имя: {user_name}\n"
            f"📱 Username: {username_info}\n\n"
            f"Связаться с клиентом: {contact_link}"
        )

        # Send notification message
        await message.bot.send_message(admin_id, notification_text)

        # Send payment screenshot
        await message.bot.send_photo(
            admin_id,
            message.photo[-1].file_id,
            caption="💰 Скриншот оплаты"
        )
    except Exception as e:
        # Log error if needed, but don't fail the user flow
        pass

    # Send confirmation to user
    await message.answer(
        "Спасибо! ✅\n\n"
        "Ваша заявка отправлена на проверку.\n"
        "Я свяжусь с вами в течение 24 часов для подтверждения консультации.",
        reply_markup=get_back_to_menu_keyboard()
    )
    await state.clear()


# Auto-funnel callbacks
@router.callback_query(F.data == CB_FUNNEL_YES)
async def funnel_day7_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Отлично! Начнём запись на консультацию.\n\n"
        "1️⃣ Как тебя зовут?\n(Напиши своё имя)",
        reply_markup=None
    )
    await state.set_state(ConsultationForm.waiting_for_name)
    await callback.answer()


@router.callback_query(F.data == CB_FUNNEL_NO)
async def funnel_day7_no(callback: CallbackQuery, repo: RequestsRepo):
    # Mark as declined
    await repo.users.update(
        callback.from_user.id,
        consultation_declined=True
    )

    await callback.message.edit_text(
        "Хорошо, понимаю! 💜\n\n"
        "Если когда-нибудь решишь — ты всегда можешь написать мне.\n\n"
        "Буду рада видеть тебя в канале ❤️\n\n"
        "https://t.me/ambasadorsvobody",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()
