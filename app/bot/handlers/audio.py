from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.bot.utils.context_utils import load_user
from app.ai.ai import get_ai
from app.bot.lang.language import get_text
from app.config.constants import (
    VALUE_DESCRIPTION,
    VALUE_AUDIO_TRANSCRIPTION,
    VALUE_AUDIO_SPEECH,
)
from app.logger import log_info, log_error
from app.database.repositories.user_repo import (
    process_request_and_debit,
    process_refund,
)


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    ai = get_ai()
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    last_response = context.user_data.get("last_response")
    if not last_response:
        await update.message.reply_text(
            get_text("pt_BR", "messages.user-message.no-audio")
        )
        return

    valid = process_request_and_debit(user, VALUE_AUDIO_SPEECH)
    if not valid:
        await update.message.reply_text(
            get_text("pt_BR", "messages.user-message.no-credits")
        )
        return

    await update.message.reply_text(
        get_text("pt_BR", "messages.user-message.audio-processing")
    )
    for res in last_response:
        retries = 2
        while retries > 0:
            try:
                audio = await ai["speech"].generate_tts(res)
                break
            except Exception as e:
                log_error("[ERROR] An error occurred:", e)
                process_refund(user, VALUE_AUDIO_SPEECH)
                retries -= 1
                if retries == 0:
                    await update.message.reply_text(
                        get_text("pt_BR", "messages.user-message.audio-error").format(
                            user_balance=user.credit_balance
                        )
                    )
                    return
        try:
            await update.message.reply_voice(voice=audio)
        except Exception as e:
            log_error("[ERROR] An error occurred:", e)
            process_refund(user, VALUE_AUDIO_SPEECH)
            await update.message.reply_text(
                get_text("pt_BR", "messages.user-message.audio-error").format(
                    user_balance=user.credit_balance
                )
            )
            return

    context.user_data["last_response"] = None
    await update.message.reply_text(
        get_text("pt_BR", "messages.menu").format(
            user_balance=user.credit_balance if user else 0,
            value_description=VALUE_DESCRIPTION,
            value_audio=VALUE_AUDIO_TRANSCRIPTION,
        )
    )
