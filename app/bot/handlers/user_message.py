from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_msg = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_text("Understood")
