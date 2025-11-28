from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.payments.payment import generate_pix

from app.bot.utils.context_utils import (
    load_user
)

from app.bot.lang.language import get_text

credit_cards = [
    {
        "credits": 100,
        "price": 1.99,
    },{
        "credits": 300,
        "price": 4.99,
    },{
        "credits": 1000,
        "price": 14.90,
    },{
        "credits": 5000,
        "price": 69.90,
    }
]

async def handle_credits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    keyboard = [
        [
            InlineKeyboardButton(get_text('pt_BR', 'messages.credits.item').format(c['credits'], f"{c['price']:,.2f}"),
                            callback_data=f"buy_{c['credits']}")]
        for c in credit_cards
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(get_text('pt_BR', 'messages.credits.title').format(user.credit_balance), reply_markup=reply_markup)

async def handle_credits_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    message = update.callback_query.message
    await query.answer()

    user = load_user(update, context)
    if not user:
        await query.edit_message_text(get_text("pt_BR", "messages.unknown-user"))
        return

    quantity = query.data.split('_')[1]
    card = None
    for c in credit_cards:
        if c["credits"] == float(quantity):
            card = c
    if not card:
        await query.edit_message_text(get_text("pt_BR", "messages.credits.error-pix"))
        return

    status, copiaecola, pgid = generate_pix(value=card['price'], email=f"user{user.uuid}@gmail.com")
    if status:
        await message.reply_text(get_text("pt_BR", "messages.credits.show-pix"))
        await message.reply_text(copiaecola)
        await message.reply_text(get_text('pt_BR', 'messages.credits.check-payment'))
    else:
        await message.reply_text(get_text("pt_BR", "messages.credits.error-pix"))


async def handle_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    if user:
        await update.message.reply_text(get_text("pt_BR", "messages.payments.payments-menu").format(credit_balance=user.credit_balance))
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))