from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from app.bot.utils.context_utils import (
    load_user
)
from app.llm.llm_factory import get_llm
from app.bot.lang.language import get_text

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    llm = get_llm()
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    if user:
        if not user.last_response:
            await update.message.reply_text(get_text("pt_BR", "messages.user-message.audio-error"))
            return

        await update.message.reply_text(get_text("pt_BR", "messages.user-message.audio-processing"))
        for res in user.last_response:
            retries = 2
            while retries > 0:
                try:
                    audio = await llm.generate_tts(res)
                    break
                except Exception as e:
                    retries -= 1
                    if retries == 0:
                        await update.message.reply_text(get_text("pt_BR", "messages.user-message.audio-error"))
                        return
            await update.message.reply_voice(voice=audio)
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.unknown-user"))


