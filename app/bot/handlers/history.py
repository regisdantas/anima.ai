from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.bot.utils.context_utils import load_user
from app.logger import log_info
from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.lang.language import get_text
from app.database.repositories.history_repo import get_last_history_by_telegram_id


async def handle_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if user:
        await update.message.reply_text(
            get_text("pt_BR", "messages.history.history-menu")
        )
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))

    history = get_last_history_by_telegram_id(user.telegram_id)
    log_info(history)
    if history:
        await update.message.reply_text(history)

    await update.message.reply_text(
        get_text("pt_BR", "messages.menu").format(
            user_balance=user.credit_balance if user else 0,
            value_description=VALUE_DESCRIPTION,
            value_audio=VALUE_AUDIO_TRANSCRIPTION,
        )
    )
