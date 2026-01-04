from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Callback data constants
CB_GET_GUIDE = "get_guide"
CB_ABOUT_ME = "about_me"
CB_CONSULTATION = "consultation"
CB_SUBSCRIBE_CHANNEL = "subscribe_channel"
CB_BACK_TO_MENU = "back_to_menu"
CB_BOOK_CONSULTATION = "book_consultation"
CB_ASK_QUESTION = "ask_question"

# Consultation form situation options
CB_SITUATION_TOXIC = "situation_toxic"
CB_SITUATION_SINGLE_MOM = "situation_single_mom"
CB_SITUATION_BURNOUT = "situation_burnout"
CB_SITUATION_WANT_RELOCATE = "situation_relocate"
CB_SITUATION_CUSTOM = "situation_custom"

# Consultation form concern options
CB_CONCERN_FINANCES = "concern_finances"
CB_CONCERN_FEARS = "concern_fears"
CB_CONCERN_DONT_KNOW = "concern_dont_know"
CB_CONCERN_FAMILY = "concern_family"
CB_CONCERN_CUSTOM = "concern_custom"

# Payment and auto-funnel
CB_PAY_CONSULTATION = "pay_consultation"
CB_PAID_SCREENSHOT = "paid_screenshot"
CB_FUNNEL_YES = "funnel_yes"
CB_FUNNEL_NO = "funnel_no"

# Shop and products
CB_SHOP = "shop"
CB_BUY_PAID_PDF = "buy_paid_pdf"
CB_BUY_COMMUNITY = "buy_community"
CB_BUY_CONSULTATION_300 = "buy_consultation_300"

# Promo codes
CB_PROMO_VIETNAM15 = "promo_vietnam15"
CB_PROMO_DREAMER20 = "promo_dreamer20"
CB_PROMO_READY15 = "promo_ready15"
CB_PROMO_NONE = "promo_none"

# Payment confirmation
CB_SEND_PAYMENT_SCREENSHOT = "send_payment_screenshot"

# Admin payment approval
CB_ADMIN_APPROVE_PAYMENT = "admin_approve_payment"
CB_ADMIN_REJECT_PAYMENT = "admin_reject_payment"


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard with 3 options"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 Получить гайд по Вьетнаму", callback_data=CB_GET_GUIDE)
    )
    builder.row(
        InlineKeyboardButton(text="📖 Узнать больше обо мне", callback_data=CB_ABOUT_ME)
    )
    builder.row(
        InlineKeyboardButton(text="💬 Записаться на консультацию", callback_data=CB_CONSULTATION)
    )
    return builder.as_markup()


def get_after_guide_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown after downloading the guide"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💜 Подписаться на канал", url="https://t.me/ambasadorsvobody")
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться в меню", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_after_story_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown after full story"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 Получить гайд по Вьетнаму", callback_data=CB_GET_GUIDE)
    )
    builder.row(
        InlineKeyboardButton(text="💬 Записаться на консультацию", callback_data=CB_CONSULTATION)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться в меню", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_consultation_keyboard() -> InlineKeyboardMarkup:
    """Consultation info keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Записаться и оплатить (500₽)", callback_data=CB_BOOK_CONSULTATION)
    )
    builder.row(
        InlineKeyboardButton(text="❓ Задать вопрос перед записью", callback_data=CB_ASK_QUESTION)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться в меню", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_situation_keyboard() -> InlineKeyboardMarkup:
    """Situation selection keyboard for consultation form"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💔 В токсичных отношениях", callback_data=CB_SITUATION_TOXIC)
    )
    builder.row(
        InlineKeyboardButton(text="👶 Мама-одиночка / после развода", callback_data=CB_SITUATION_SINGLE_MOM)
    )
    builder.row(
        InlineKeyboardButton(text="💼 Выгорание на работе / в системе", callback_data=CB_SITUATION_BURNOUT)
    )
    builder.row(
        InlineKeyboardButton(text="🌍 Просто хочу переехать", callback_data=CB_SITUATION_WANT_RELOCATE)
    )
    builder.row(
        InlineKeyboardButton(text="✍️ Напишу сама", callback_data=CB_SITUATION_CUSTOM)
    )
    return builder.as_markup()


def get_concern_keyboard() -> InlineKeyboardMarkup:
    """Concern selection keyboard for consultation form"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💰 Финансы / нет денег", callback_data=CB_CONCERN_FINANCES)
    )
    builder.row(
        InlineKeyboardButton(text="😰 Страхи и неуверенность", callback_data=CB_CONCERN_FEARS)
    )
    builder.row(
        InlineKeyboardButton(text="📋 Не знаю с чего начать", callback_data=CB_CONCERN_DONT_KNOW)
    )
    builder.row(
        InlineKeyboardButton(text="👨‍👩‍👧 Дети / семья держит", callback_data=CB_CONCERN_FAMILY)
    )
    builder.row(
        InlineKeyboardButton(text="✍️ Напишу сама", callback_data=CB_CONCERN_CUSTOM)
    )
    return builder.as_markup()


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Payment keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Оплатить 500₽", callback_data=CB_PAY_CONSULTATION)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться назад", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_payment_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Keyboard after showing payment details"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Я оплатила, вот скриншот", callback_data=CB_PAID_SCREENSHOT)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться назад", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_auto_funnel_day7_keyboard() -> InlineKeyboardMarkup:
    """Day 7 auto-funnel keyboard (yes/no for consultation)"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да, записываюсь за 500₽", callback_data=CB_FUNNEL_YES)
    )
    builder.row(
        InlineKeyboardButton(text="❌ Нет, спасибо", callback_data=CB_FUNNEL_NO)
    )
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Simple back to menu keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_day2_keyboard() -> InlineKeyboardMarkup:
    """Day 2 auto-funnel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💬 Записаться на консультацию", callback_data=CB_CONSULTATION)
    )
    return builder.as_markup()


def get_day0_keyboard() -> InlineKeyboardMarkup:
    """Day 0 auto-funnel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💜 Подписаться на канал", url="https://t.me/ambasadorsvobody")
    )
    return builder.as_markup()


# Shop and Products keyboards

def get_shop_keyboard() -> InlineKeyboardMarkup:
    """Shop menu with all paid products"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📕 Полный гайд по релокации ($50)", callback_data=CB_BUY_PAID_PDF)
    )
    builder.row(
        InlineKeyboardButton(text="👭 Сообщество ($30/мес)", callback_data=CB_BUY_COMMUNITY)
    )
    builder.row(
        InlineKeyboardButton(text="💎 Расширенная консультация ($300)", callback_data=CB_BUY_CONSULTATION_300)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться в меню", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_promo_keyboard() -> InlineKeyboardMarkup:
    """Promo code selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 VIETNAM15 (-15%)", callback_data=CB_PROMO_VIETNAM15)
    )
    builder.row(
        InlineKeyboardButton(text="✨ DREAMER20 (-20%)", callback_data=CB_PROMO_DREAMER20)
    )
    builder.row(
        InlineKeyboardButton(text="🔥 READY15 (-15%)", callback_data=CB_PROMO_READY15)
    )
    builder.row(
        InlineKeyboardButton(text="❌ Без промокода", callback_data=CB_PROMO_NONE)
    )
    return builder.as_markup()


def get_payment_instructions_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown after payment instructions"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Я оплатила, отправить скриншот", callback_data=CB_SEND_PAYMENT_SCREENSHOT)
    )
    builder.row(
        InlineKeyboardButton(text="← Вернуться назад", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_upsell_community_keyboard() -> InlineKeyboardMarkup:
    """Upsell keyboard for community after quiz"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👭 Да, хочу в сообщество!", callback_data=CB_BUY_COMMUNITY)
    )
    builder.row(
        InlineKeyboardButton(text="Может позже", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_upsell_paid_pdf_keyboard() -> InlineKeyboardMarkup:
    """Upsell keyboard for paid PDF after free guide"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📕 Да, хочу полный гайд!", callback_data=CB_BUY_PAID_PDF)
    )
    builder.row(
        InlineKeyboardButton(text="Спасибо, пока хватит", callback_data=CB_BACK_TO_MENU)
    )
    return builder.as_markup()


def get_admin_payment_approval_keyboard(payment_id: int) -> InlineKeyboardMarkup:
    """Admin keyboard for approving/rejecting payments"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✅ Подтвердить",
            callback_data=f"{CB_ADMIN_APPROVE_PAYMENT}:{payment_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="❌ Отклонить",
            callback_data=f"{CB_ADMIN_REJECT_PAYMENT}:{payment_id}"
        )
    )
    return builder.as_markup()
