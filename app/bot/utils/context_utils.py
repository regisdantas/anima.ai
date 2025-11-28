from telegram import Update
from telegram.ext import ContextTypes
from app.database.models.user import User
from app.logger import log_info, log_error

def get_message_obj(update: Update):
    if update.message:
        return update.message
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message
    return None


def load_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = get_message_obj(update)
        if not message:
            return None

        user = context.user_data.get("user")

        if user is None:
            telegram_id = message.from_user.id
            name = message.from_user.first_name

            user = User(
                telegram_id=telegram_id,
                name=name
            )
            user.add_credits(100)
            context.user_data["user"] = user

        return user

    except Exception as e:
        log_error("[ERROR] An error occurred:", e)
        return None
