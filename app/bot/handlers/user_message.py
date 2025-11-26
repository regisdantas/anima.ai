from typing import Any, cast

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.anima.models.user import User
from app.anima.dream_pipeline import handle_dream
from app.bot.utils.context_utils import (
    get_message_obj,
    load_user
)

from app.bot.lang.lang_loader import get_language
language = get_language()

async def send_response(user: User, result: str, metadata: Any):
    update = cast(Update, metadata)
    await update.message.reply_text(result)

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    if user:
        user_msg = update.message.text
        interpret_message = f"Ok, {user.name}! Let me try to interpret this one."
        await update.message.reply_text(interpret_message)
        await handle_dream(user, user_msg, send_response, update)

    else:
        await update.message.reply_text("I could not locate your user ID.")

