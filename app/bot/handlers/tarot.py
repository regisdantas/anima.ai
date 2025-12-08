from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.bot.lang.language import get_text
from app.bot.utils.context_utils import load_user
from app.config.constants import VALUE_TAROT_READING, VALUE_AUDIO_SPEECH
from app.database.repositories.user_repo import (
    process_request_and_debit,
    process_refund,
)
from app.database.repositories.history_repo import (
    get_history_by_telegram_id,
    create_history,
)
from app.anima.anima_pipeline import handle_tarot_pipeline


from typing import Any, cast
from app.database.models.user import User
from app.logger import log_info, log_error


async def send_response(user: User, result: dict, metadata: dict):
    update = cast(Update, metadata.get("update"))
    context = cast(ContextTypes.DEFAULT_TYPE, metadata.get("context"))
    card = result.get("card")
    context.user_data["last_response"] = card

    summary = result.get("summary")
    create_history(
        user_id=user.uuid,
        telegram_id=user.telegram_id,
        message_type="tarot",
        content=summary,
    )

    for res in card:
        await update.message.reply_text(res)

    audio_offer_message = get_text("pt_BR", "messages.user-message.audio-offer").format(
        value=VALUE_AUDIO_SPEECH
    )
    await update.message.reply_text(audio_offer_message)


async def handle_tarot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    user_query = " ".join(context.args)
    user_msg = user_query.strip()
    if not user_msg:
        no_question_message = get_text("pt_BR", "messages.tarot.no-question").format(
            user_name=user.name
        )
        await update.message.reply_text(no_question_message)
        return

    valid = process_request_and_debit(user, VALUE_TAROT_READING)
    if not valid:
        await update.message.reply_text(get_text("pt_BR", "messages.tarot.no-credits"))
        return

    try:
        interpret_message = get_text("pt_BR", "messages.tarot.question-ok").format(
            user_name=user.name
        )
        await update.message.reply_text(interpret_message)
        history = get_history_by_telegram_id(telegram_id=user.telegram_id, count=4)
        history.reverse()
        await handle_tarot_pipeline(
            user,
            user_msg,
            history,
            send_response,
            {"update": update, "context": context},
        )

    except Exception as e:
        log_error(e)
        process_refund(user, VALUE_TAROT_READING)
        await update.message.reply_text(
            get_text("pt_BR", "messages.tarot.error").format(
                user_balance=user.credit_balance
            )
        )
