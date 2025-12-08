from telegram import Update
from telegram.ext import ContextTypes
from app.database.repositories.user_repo import get_all_users
from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.lang.language import get_text


async def handle_morning(context: ContextTypes.DEFAULT_TYPE) -> None:
    user_list = get_all_users()
    for user in user_list:
        if user.silence:
            continue
        await context.bot.send_message(
            user.telegram_id,
            get_text("pt_BR", "messages.daily-morning").format(user_name=user.name),
        )
        await context.bot.send_message(
            user.telegram_id,
            get_text("pt_BR", "messages.menu").format(
                user_balance=user.credit_balance if user else 0,
                value_description=VALUE_DESCRIPTION,
                value_audio=VALUE_AUDIO_TRANSCRIPTION,
            ),
        )
