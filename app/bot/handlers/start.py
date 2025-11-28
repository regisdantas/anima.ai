from telegram import Update
from telegram.ext import ContextTypes
from app.database.models import user
from app.bot.utils.context_utils import (
    get_message_obj,
    load_user
)

from app.bot.lang.language import get_text

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    if user: 
        await update.message.reply_text(get_text("pt_BR", "messages.welcome.known-user").format(user_name=user.name))
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.welcome.new-user"))
    await update.message.reply_text(get_text("pt_BR", "messages.welcome.welcome-message").format(value_description=25, value_audio=40))


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_text("pt_BR", "messages.welcome.welcome-message").format(value_description=25, value_audio=40))