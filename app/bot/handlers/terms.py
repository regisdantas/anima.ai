from telegram import Update
from telegram.ext import ContextTypes

from app.bot.lang.language import get_text

async def handle_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_text("pt_BR", "messages.terms.terms-and-conditions"))

async def handle_accept_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_text("pt_BR", "messages.terms.accepted-terms"))

async def handle_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_text("pt_BR", "messages.terms.delete"))