from telegram import Update
from telegram.ext import ContextTypes

from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.lang.language import get_text
from app.bot.utils.context_utils import load_user
from app.database.repositories.history_repo import delete_history_by_telegram


async def handle_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)

    await update.message.reply_text(
        get_text("pt_BR", "messages.terms.terms-and-conditions")
    )

    await update.message.reply_text(
        get_text("pt_BR", "messages.menu").format(
            user_balance=user.credit_balance if user else 0,
            value_description=VALUE_DESCRIPTION,
            value_audio=VALUE_AUDIO_TRANSCRIPTION,
        )
    )


async def handle_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    delete_history_by_telegram(telegram_id=update.message.chat_id)
    await update.message.reply_text(get_text("pt_BR", "messages.terms.delete"))
