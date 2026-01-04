"""User product purchase handlers"""
from decimal import Decimal

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from infrastructure.database.requests import RequestsRepo
from keyboards.inline import (
    get_shop_keyboard, get_promo_keyboard, get_payment_instructions_keyboard,
    get_back_to_menu_keyboard,
    CB_SHOP, CB_BUY_PAID_PDF, CB_BUY_COMMUNITY, CB_BUY_CONSULTATION_300,
    CB_PROMO_VIETNAM15, CB_PROMO_DREAMER20, CB_PROMO_READY15, CB_PROMO_NONE,
    CB_SEND_PAYMENT_SCREENSHOT
)
from services.payment_processor import calculate_price
from utils.constants import (
    PRODUCT_PAID_PDF, PRODUCT_COMMUNITY, PRODUCT_CONSULTATION_300,
    PRODUCT_DESCRIPTIONS, PRODUCT_NAMES,
    SBERBANK_CARD, SBERBANK_RECIPIENT
)
from utils.states import PurchaseStates

router = Router()


@router.callback_query(F.data == CB_SHOP)
async def shop_handler(callback: CallbackQuery):
    """Show shop with all products"""
    shop_text = """🛍️ **МАГАЗИН ПРОДУКТОВ**

Здесь ты найдешь всё для успешной релокации!

Выбирай продукт, чтобы узнать подробности и купить:"""

    await callback.message.edit_text(shop_text, reply_markup=get_shop_keyboard(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == CB_BUY_PAID_PDF)
async def buy_paid_pdf_handler(callback: CallbackQuery, state: FSMContext):
    """Start purchase of paid PDF"""
    await start_purchase(
        callback,
        state,
        PRODUCT_PAID_PDF,
        PRODUCT_DESCRIPTIONS[PRODUCT_PAID_PDF]
    )


@router.callback_query(F.data == CB_BUY_COMMUNITY)
async def buy_community_handler(callback: CallbackQuery, state: FSMContext):
    """Start purchase of community access"""
    await start_purchase(
        callback,
        state,
        PRODUCT_COMMUNITY,
        PRODUCT_DESCRIPTIONS[PRODUCT_COMMUNITY]
    )


@router.callback_query(F.data == CB_BUY_CONSULTATION_300)
async def buy_consultation_300_handler(callback: CallbackQuery, state: FSMContext):
    """Start purchase of extended consultation"""
    await start_purchase(
        callback,
        state,
        PRODUCT_CONSULTATION_300,
        PRODUCT_DESCRIPTIONS[PRODUCT_CONSULTATION_300]
    )


async def start_purchase(callback: CallbackQuery, state: FSMContext, product_type: str, description: str):
    """
    Common function to start purchase flow.

    Flow: Product description -> Promo code selection -> Payment instructions -> Screenshot
    """
    # Save product type to state
    await state.update_data(product_type=product_type)

    # Show product description
    text = f"{description}\n\n💳 **Готова оформить покупку?**\n\nВыбери промокод, если есть:"

    await callback.message.edit_text(text, reply_markup=get_promo_keyboard(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.in_([CB_PROMO_VIETNAM15, CB_PROMO_DREAMER20, CB_PROMO_READY15, CB_PROMO_NONE]))
async def apply_promo_handler(callback: CallbackQuery, state: FSMContext):
    """Apply promo code and show payment instructions"""
    # Get selected promo
    promo_map = {
        CB_PROMO_VIETNAM15: "VIETNAM15",
        CB_PROMO_DREAMER20: "DREAMER20",
        CB_PROMO_READY15: "READY15",
        CB_PROMO_NONE: None
    }

    promo_code = promo_map.get(callback.data)
    data = await state.get_data()
    product_type = data.get("product_type")

    if not product_type:
        await callback.answer("❌ Ошибка: продукт не выбран", show_alert=True)
        return

    # Calculate price
    final_price, discount_percent = calculate_price(product_type, promo_code)

    # Save to state
    await state.update_data(
        promo_code=promo_code,
        final_price=float(final_price),
        discount_percent=discount_percent
    )

    # Show payment instructions
    product_name = PRODUCT_NAMES[product_type]

    if promo_code:
        price_text = (
            f"~~${calculate_price(product_type)[0]}~~ → **${final_price}** "
            f"(скидка {discount_percent}% по промокоду {promo_code})"
        )
    else:
        price_text = f"**${final_price}**"

    payment_text = f"""💳 **ОПЛАТА: {product_name}**

Цена: {price_text}

**Реквизиты для оплаты:**

💳 Карта: `{SBERBANK_CARD}`
👤 Получатель: {SBERBANK_RECIPIENT}

**Как оплатить:**

1️⃣ Переведи {final_price} USD на карту выше
2️⃣ Сделай скриншот подтверждения оплаты
3️⃣ Нажми кнопку ниже и отправь скриншот

⏰ Проверка платежа займет до 24 часов.
После подтверждения получишь доступ к продукту!

❓ Вопросы? Пиши мне в личку!"""

    await callback.message.edit_text(
        payment_text,
        reply_markup=get_payment_instructions_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == CB_SEND_PAYMENT_SCREENSHOT)
async def send_screenshot_prompt(callback: CallbackQuery, state: FSMContext):
    """Prompt user to send payment screenshot"""
    await callback.message.edit_text(
        "📸 **ОТПРАВЬ СКРИНШОТ ОПЛАТЫ**\n\n"
        "Пришли мне скриншот подтверждения платежа.\n\n"
        "Я проверю его и активирую доступ к продукту в течение 24 часов! ⏰",
        reply_markup=None,
        parse_mode="Markdown"
    )
    await state.set_state(PurchaseStates.waiting_for_screenshot)
    await callback.answer()


@router.message(PurchaseStates.waiting_for_screenshot, F.photo)
async def process_payment_screenshot(message: Message, state: FSMContext, repo: RequestsRepo, config):
    """Process payment screenshot and create pending payment"""
    data = await state.get_data()
    product_type = data.get("product_type")
    promo_code = data.get("promo_code")
    final_price = data.get("final_price")
    discount_percent = data.get("discount_percent", 0)

    if not product_type or final_price is None:
        await message.answer(
            "❌ Ошибка: данные о покупке не найдены. Начни заново из магазина.",
            reply_markup=get_back_to_menu_keyboard()
        )
        await state.clear()
        return

    # Get original price
    base_price, _ = calculate_price(product_type)

    # Save screenshot file_id
    screenshot_file_id = message.photo[-1].file_id

    # Create pending payment
    await repo.payments.create(
        user_id=message.from_user.id,
        product_type=product_type,
        amount_usd=Decimal(str(base_price)),
        promo_code=promo_code,
        discount_percent=discount_percent,
        final_amount_usd=Decimal(str(final_price)),
        screenshot_file_id=screenshot_file_id,
        status="pending"
    )

    # Get user info
    user = await repo.users.get(message.from_user.id)
    user_name = user.first_name if user else message.from_user.first_name
    username_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"

    # Notify admin
    admin_ids = config.bot.admin_ids
    print(f"🔍 Admin IDs: {admin_ids}")
    print(f"🔍 User ID who sent screenshot: {message.from_user.id}")

    if admin_ids:
        product_name = PRODUCT_NAMES[product_type]

        for admin_id in admin_ids:
            try:
                notification_text = (
                    f"🔔 **НОВЫЙ ПЛАТЕЖ НА ПРОВЕРКУ!**\n\n"
                    f"👤 Пользователь: {user_name}\n"
                    f"📱 Username: {username_info}\n"
                    f"🛍️ Продукт: {product_name}\n"
                    f"💰 Сумма: ${final_price}\n"
                )

                if promo_code:
                    notification_text += f"🎁 Промокод: {promo_code} (-{discount_percent}%)\n"

                notification_text += (
                    f"\n**Действия:**\n"
                    f"✅ Подтвердить: `/approve {message.from_user.id}`\n"
                    f"❌ Отклонить: `/reject {message.from_user.id}`"
                )

                print(f"📤 Sending notification to admin {admin_id}...")
                await message.bot.send_message(
                    admin_id,
                    notification_text,
                    parse_mode="Markdown"
                )

                # Send screenshot
                print(f"📸 Sending screenshot to admin {admin_id}...")
                await message.bot.send_photo(
                    admin_id,
                    screenshot_file_id,
                    caption="💳 Скриншот оплаты"
                )
                print(f"✅ Successfully sent notification to admin {admin_id}")
            except Exception as e:
                # Log error but don't fail user flow
                print(f"❌ Ошибка отправки уведомления админу {admin_id}: {e}")
    else:
        print(f"⚠️ No admin IDs configured!")

    # Send confirmation to user
    await message.answer(
        "✅ **СКРИНШОТ ПОЛУЧЕН!**\n\n"
        "Твоя заявка отправлена на проверку.\n\n"
        "⏰ Я проверю платеж и активирую доступ в течение 24 часов.\n\n"
        "Спасибо за покупку! 💜",
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown"
    )

    await state.clear()


@router.message(PurchaseStates.waiting_for_screenshot)
async def handle_non_photo(message: Message):
    """Handle non-photo messages when screenshot expected"""
    await message.answer(
        "❌ Пожалуйста, отправь **скриншот** (изображение) подтверждения оплаты.\n\n"
        "Не текст, а именно фото!",
        parse_mode="Markdown"
    )
