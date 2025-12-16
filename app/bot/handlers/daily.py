from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from app.database.repositories.user_repo import get_all_users, update_user_silence
from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.lang.language import get_text
from app.bot.utils.utils import get_random
from app.logger import log_info


async def handle_morning(context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info("Morning job executed. Sending messages to all users.")
    user_list = get_all_users()
    for user in user_list:
        log_info(f"Sending message to user: {user.name}. User silence: {user.silence}")
        if user.silence:
            continue
        inspiration = get_random(get_text("pt_BR", "messages.daily.inspirations"))
        try:
            await context.bot.send_message(
                user.telegram_id,
                get_text("pt_BR", "messages.daily.morning").format(
                    user_name=user.name, inspiration=inspiration
                ),
            )
        except Forbidden:
            log_info(f"User {user.name} has blocked the bot. Updating silence status.")
            update_user_silence(user, True)
        except Exception as e:
            log_info(
                f"Failed to send morning message to user: {user.name}. Exception: {e}"
            )

    log_info("Morning job completed.")
