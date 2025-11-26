from typing import Any, cast

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.anima.models.user import User
from app.anima.dream_pipeline import handle_dream
from app.bot.utils.context_utils import (
    load_user
)
from app.llm.llm_factory import get_llm
from app.bot.lang.language import get_text

async def send_response(user: User, result: list[str], metadata: Any):
    llm = get_llm()
    update = cast(Update, metadata)
    for res in result:
        await update.message.reply_text(res)

    audio_offer_message = get_text("pt_BR", "messages.user-message.audio-offer")
    await update.message.reply_text(audio_offer_message)

    audio = await llm.generate_tts("\n".join(result))
    await update.message.reply_voice(voice=audio)

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    if user:
        user_msg = update.message.text
        if len(user_msg) < 10:
            too_short_message = get_text("pt_BR", "messages.user-message.prompt-too-short").format(user_name=user.name)
            await update.message.reply_text(too_short_message)
            return

        interpret_message = get_text("pt_BR", "messages.user-message.prompt-ok").format(user_name=user.name)
        await update.message.reply_text(interpret_message)
        await handle_dream(user, user_msg, send_response, update)
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))

