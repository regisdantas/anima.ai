from telegram import Update
from telegram.ext import ContextTypes

async def handle_credits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Credits Menu")

async def handle_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Payments Menu")