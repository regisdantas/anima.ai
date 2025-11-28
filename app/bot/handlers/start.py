from telegram import Update
from telegram.ext import ContextTypes
from app.bot.utils.context_utils import load_user

from app.bot.lang.language import get_text


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    if user:
        await update.message.reply_text(
            get_text("pt_BR", "messages.welcome.known-user").format(user_name=user.name)
        )
    else:
        await update.message.reply_text(get_text("pt_BR", "messages.welcome.new-user"))
    await update.message.reply_text(
        get_text("pt_BR", "messages.welcome.welcome-message").format(
            user_balance=user.credit_balance, value_description=25, value_audio=40
        )
    )


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    await update.message.reply_text(
        get_text("pt_BR", "messages.welcome.welcome-message").format(
            user_balance=user.credit_balance, value_description=25, value_audio=40
        )
    )
