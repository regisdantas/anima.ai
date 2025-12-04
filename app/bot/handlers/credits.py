from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.payments.payment import generate_pix, check_payment

from app.database.models.payment import Payment
from app.database.repositories.payment_repo import (
    create_payment,
    get_payment_pending_by_telegram_id,
    update_payment_status,
)
from app.database.repositories.user_repo import update_user_credits
from app.bot.utils.context_utils import load_user
from app.bot.utils.utils import generate_qr_code

from app.bot.lang.language import get_text

credit_cards = [
    {
        "credits": 100,
        "price": 1.99,
    },
    {
        "credits": 300,
        "price": 4.99,
    },
    {
        "credits": 1000,
        "price": 14.90,
    },
    {
        "credits": 5000,
        "price": 69.90,
    },
]


async def update_payments(
    update: Update, context: ContextTypes.DEFAULT_TYPE, payments
) -> None:
    user = load_user(update, context)
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    for pay in payments:
        if pay.status == "pending":
            new_status = check_payment(pay.payment_id)
            if new_status != pay.status:
                pay.status = new_status
                update_payment_status(pay.payment_id, new_status)
                update_user_credits(pay.telegram_id, user.credit_balance + pay.credits)
                await update.message.reply_text(
                    get_text("pt_BR", "messages.credits.bought").format(pay.credits)
                )


async def handle_credits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payments = get_payment_pending_by_telegram_id(update.message.chat.id)
    if payments:
        await update_payments(update, context, payments)

    user = load_user(update, context)
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    keyboard = [
        [
            InlineKeyboardButton(
                get_text("pt_BR", "messages.credits.item").format(
                    c["credits"], f"{c['price']:,.2f}"
                ),
                callback_data=f"buy_{c['credits']}",
            )
        ]
        for c in credit_cards
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        get_text("pt_BR", "messages.credits.title").format(user.credit_balance),
        reply_markup=reply_markup,
    )


async def handle_credits_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    message = update.callback_query.message
    await query.answer()

    user = load_user(update, context)
    if not user:
        await query.edit_message_text(get_text("pt_BR", "messages.unknown-user"))
        return

    quantity = query.data.split("_")[1]
    card = None
    for c in credit_cards:
        if c["credits"] == float(quantity):
            card = c
    if not card:
        await query.edit_message_text(get_text("pt_BR", "messages.credits.error-pix"))
        return

    status, copiaecola, pgid = generate_pix(
        value=card["price"], email=f"user{user.telegram_id}@gmail.com"
    )
    if status:
        create_payment(
            Payment(
                id=None,
                user_id=user.uuid,
                telegram_id=user.telegram_id,
                payment_id=pgid,
                credits=card["credits"],
                status="pending",
            )
        )
        await message.reply_text(get_text("pt_BR", "messages.credits.show-pix"))
        await context.application.bot.send_photo(
            chat_id=user.telegram_id, photo=generate_qr_code(copiaecola)
        )
        await message.reply_text(copiaecola)
        await message.reply_text(get_text("pt_BR", "messages.credits.check-payment"))
    else:
        await message.reply_text(get_text("pt_BR", "messages.credits.error-pix"))


async def handle_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    payments = get_payment_pending_by_telegram_id(user.telegram_id)
    if not payments:
        await update.message.reply_text("🔍 Você não possui pagamentos pendentes.")
        return
    await update_payments(update, context, payments)

    menu_pagamentos = "📜 **Pagamentos Pendentes** 📜\n\n"
    for pay in payments:
        menu_pagamentos += (
            f"🆔    ID:               {pay.payment_id}\n"
            f"💰    Créditos:    {pay.credits}\n"
            f"📅    Data:           {pay.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"❓    Status:        {pay.status}\n\n"
        )
    await update.message.reply_text(menu_pagamentos)
