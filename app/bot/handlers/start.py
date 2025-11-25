from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first_name = update.effective_user.first_name
    welcome_message = f"Hello, {user_first_name}! Welcome to Anima AI Bot."
    await update.message.reply_text(welcome_message)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help Menu")