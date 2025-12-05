from typing import Any, cast
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.ai.ai import get_ai
from app.database.models.user import User
from app.anima.dream_pipeline import handle_dream
from app.bot.utils.context_utils import load_user
from app.bot.lang.language import get_text
from app.logger import log_info, log_error
from app.database.repositories.user_repo import (
    process_request_and_debit,
    process_refund,
)
from app.database.repositories.history_repo import (
    create_history,
    get_history_by_telegram_id,
)
from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_SPEECH


async def send_response(user: User, result: dict, metadata: dict):
    update = cast(Update, metadata.get("update"))
    context = cast(ContextTypes.DEFAULT_TYPE, metadata.get("context"))
    interpretation = result.get("interpretation")
    context.user_data["last_response"] = interpretation

    summary = result.get("summary")
    create_history(
        user_id=user.uuid,
        telegram_id=user.telegram_id,
        message_type="dream",
        content=summary,
    )

    for res in interpretation:
        await update.message.reply_text(res)

    audio_offer_message = get_text("pt_BR", "messages.user-message.audio-offer").format(
        value=VALUE_AUDIO_SPEECH
    )
    await update.message.reply_text(audio_offer_message)


async def handle_user_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    user_msg = update.message.text
    if len(user_msg) < 100:
        too_short_message = get_text(
            "pt_BR", "messages.user-message.prompt-too-short"
        ).format(user_name=user.name)
        await update.message.reply_text(too_short_message)
        return

    valid = process_request_and_debit(user.telegram_id, VALUE_DESCRIPTION)
    if not valid:
        await update.message.reply_text(
            get_text("pt_BR", "messages.user-message.no-credits")
        )
        return

    try:
        interpret_message = get_text("pt_BR", "messages.user-message.prompt-ok").format(
            user_name=user.name
        )
        await update.message.reply_text(interpret_message)
        history = get_history_by_telegram_id(telegram_id=user.telegram_id, count=4)
        await handle_dream(
            user,
            user_msg,
            history,
            send_response,
            {"update": update, "context": context},
        )

    except Exception as e:
        log_error(e)
        process_refund(user.telegram_id, VALUE_DESCRIPTION)
        await update.message.reply_text(
            get_text("pt_BR", "messages.user-message.error").format(
                user_balance=user.credit_balance
            )
        )


async def handle_voice_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = load_user(update, context)
    ai = get_ai()

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    valid = process_request_and_debit(user.telegram_id, VALUE_AUDIO)
    if not valid:
        await update.message.reply_text(
            get_text("pt_BR", "messages.user-message.no-credits-audio")
        )
        return

    voice = update.message.voice
    tg_file = await voice.get_file()
    buffer = BytesIO()
    await tg_file.download_to_memory(out=buffer)
    buffer.seek(0)

    await update.message.reply_text(
        get_text("pt_BR", "messages.user-message.transcribe-processing")
    )

    retries = 2
    while retries > 0:
        try:
            text = await ai["speech"].transcribe_audio(buffer)
            break
        except Exception as e:
            log_error(e)
            retries -= 1
            if retries == 0:
                process_refund(user.telegram_id, VALUE_AUDIO)
                await update.message.reply_text(
                    get_text("pt_BR", "messages.user-message.transcribe-error").format(
                        user_balance=user.credit_balance
                    )
                )
                return

    await update.message.reply_text(
        get_text("pt_BR", "messages.user-message.transcription") + text
    )
    interpret_message = get_text("pt_BR", "messages.user-message.prompt-ok").format(
        user_name=user.name
    )
    await update.message.reply_text(interpret_message)
    history = get_history_by_telegram_id(telegram_id=user.telegram_id, count=4)
    await handle_dream(
        user, text, history, send_response, {"update": update, "context": context}
    )
