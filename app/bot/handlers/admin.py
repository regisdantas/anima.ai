from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.database.models.user import User, check_admin
from app.bot.utils.context_utils import load_user
from app.database.repositories.user_repo import get_all_users


async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    if user and check_admin(user):
        await update.message.reply_text("Hello, Admin!")
        keyboard = [
            [
                InlineKeyboardButton(
                    f"List Users",
                    callback_data=f"admin_list_users",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Select an admin action:",
            reply_markup=reply_markup,
        )


async def handle_admin_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    user = load_user(update, context)
    if user and check_admin(user):
        await query.edit_message_text(f"Admin action executed: {query.data}")
        if query.data == "admin_list_users":
            users = get_all_users()
            user_list = "\n".join(
                [f"{u.name} ({u.telegram_id}) - {u.credit_balance}" for u in users]
            )
            await query.edit_message_text(f"Registered Users:\n{user_list}")
