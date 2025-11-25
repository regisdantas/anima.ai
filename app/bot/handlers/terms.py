from telegram import Update
from telegram.ext import ContextTypes

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Terms and Conditions")

async def accept_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You have accepted the Terms and Conditions.")

async def decline_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You have declined the Terms and Conditions.")
