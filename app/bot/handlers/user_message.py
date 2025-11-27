from typing import Any, cast
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.ai.ai import get_ai
from app.database.models.user import User
from app.anima.dream_pipeline import handle_dream
from app.bot.utils.context_utils import (
    load_user
)
from app.bot.lang.language import get_text

async def send_response(user: User, result: list[str], metadata: Any):
    update = cast(Update, metadata)
    for res in result:
        await update.message.reply_text(res)
    
    user.last_response = result

    audio_offer_message = get_text("pt_BR", "messages.user-message.audio-offer").format(value=20)
    await update.message.reply_text(audio_offer_message)

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    user_msg = update.message.text
    if len(user_msg) < 10:
        too_short_message = get_text("pt_BR", "messages.user-message.prompt-too-short").format(user_name=user.name)
        await update.message.reply_text(too_short_message)
        return

    interpret_message = get_text("pt_BR", "messages.user-message.prompt-ok").format(user_name=user.name)
    await update.message.reply_text(interpret_message)
    await handle_dream(user, user_msg, send_response, update)

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    ai = get_ai()

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    if not user:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))
        return

    voice = update.message.voice
    tg_file = await voice.get_file()
    buffer = BytesIO()
    await tg_file.download_to_memory(out=buffer)
    buffer.seek(0)

    await update.message.reply_text(get_text("pt_BR", "messages.user-message.transcribe-processing"))

    retries = 2
    while retries > 0:
        try:
            text = await ai["speech"].transcribe_audio(buffer)
            break
        except Exception as e:
            retries -= 1
            if retries == 0:
                await update.message.reply_text(get_text("pt_BR", "messages.user-message.transcribe-error"))
                return

    await update.message.reply_text(f"📝 Transcrição:\n{text}")
    interpret_message = get_text("pt_BR", "messages.user-message.prompt-ok").format(user_name=user.name)
    await update.message.reply_text(interpret_message)
    await handle_dream(user, text, send_response, update)