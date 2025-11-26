from telegram import Update
from telegram.ext import ContextTypes

from app.bot.lang.lang_loader import get_language
language = get_language()

async def handle_customize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Customization Menu")