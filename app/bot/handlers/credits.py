from telegram import Update
from telegram.ext import ContextTypes

async def credits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Credits Menu")

async def payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Payments Menu")