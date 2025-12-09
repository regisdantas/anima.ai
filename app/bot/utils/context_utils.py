from telegram import Update
from telegram.ext import ContextTypes
from app.database.models.user import User
from app.logger import log_info, log_error
from app.database.repositories.user_repo import (
    get_user_by_telegram_id,
    create_user,
)


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

        name = message.chat.first_name
        telegram_id = message.chat.id

        user = get_user_by_telegram_id(telegram_id)

        if not user:
            user = create_user(
                User(telegram_id=telegram_id, name=name, credit_balance=100)
            )
            if not user:
                raise Exception("Failed to create user")

        log_info(
            f"User {user.telegram_id} {user.name}[{user.credit_balance}]:\nMessage: {message.text}\n------------------------------------------"
        )
        return user

    except Exception as e:
        log_error("[ERROR] An error occurred:", e)
        return None
