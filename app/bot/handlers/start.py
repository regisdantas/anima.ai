from telegram import Update
from telegram.ext import ContextTypes
from app.bot.utils.context_utils import (
    get_message_obj,
    load_user
)

from app.bot.lang.lang_loader import get_language
language = get_language()

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global language
    user = load_user(update, context)
    if user: 
        await update.message.reply_text(language['messages']['known-user'].format(user_name=user.name))
    else:
        await update.message.reply_text(language['messages']['new-user'])
    await update.message.reply_text(language['messages']['welcome'])


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(language['messages']['welcome'])