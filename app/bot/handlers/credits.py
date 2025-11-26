from telegram import Update
from telegram.ext import ContextTypes

from app.bot.lang.lang_loader import get_language
language = get_language()

async def handle_credits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Credits Menu")

async def handle_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Payments Menu")