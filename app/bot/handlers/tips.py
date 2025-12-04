from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.bot.utils.context_utils import load_user

from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.lang.language import get_text


async def handle_tips(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if user:
        await update.message.reply_text(get_text("pt_BR", "messages.tips"))
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))

        user = load_user(update, context)

    await update.message.reply_text(
        get_text("pt_BR", "messages.menu").format(
            user_balance=user.credit_balance if user else 0,
            value_description=VALUE_DESCRIPTION,
            value_audio=VALUE_AUDIO_TRANSCRIPTION,
        )
    )
