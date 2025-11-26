from telegram import Update
from telegram.ext import ContextTypes

from app.bot.lang.lang_loader import get_language
language = get_language()

async def handle_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Terms and Conditions")

async def handle_accept_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You have accepted the Terms and Conditions.")

async def handle_decline_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You have declined the Terms and Conditions.")
