from telegram import Update
from telegram.ext import ContextTypes
from app.bot.utils.context_utils import (
    get_message_obj,
    load_user
)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    print(user)
    if user: 
        welcome_message = f"Hello, {user.name}! Welcome to Anima AI Bot."
        await update.message.reply_text(welcome_message)
    else:
        await update.message.reply_text("Hello. What's your name?")


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help Menu")