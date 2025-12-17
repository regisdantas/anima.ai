from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from app.database.models.user import User, check_admin
from app.bot.utils.context_utils import load_user
from app.database.repositories.user_repo import (
    get_all_users,
    get_user_by_telegram_id,
    update_user_credits,
)
from app.config.constants import VALUE_DESCRIPTION, VALUE_AUDIO_TRANSCRIPTION
from app.bot.handlers.daily import handle_morning
from app.bot.lang.language import get_text

ADMIN_CREDIT = 1


async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = load_user(update, context)
    if user and check_admin(user):
        await update.message.reply_text("Hello, Admin!")
        keyboard = [
            [
                InlineKeyboardButton(
                    f"List Users",
                    callback_data=f"admin_list_users",
                ),
                InlineKeyboardButton(
                    f"Morning",
                    callback_data=f"admin_morning",
                ),
                InlineKeyboardButton(
                    f"Credit User",
                    callback_data=f"admin_credit_user",
                ),
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
            await query.edit_message_text(f"{user_list}")
        elif query.data == "admin_morning":
            await handle_morning(context)
            await query.edit_message_text("Morning messages sent to all users.")
        elif query.data == "admin_credit_user":
            await query.edit_message_text(
                "Please provide the Telegram ID and amount to credit in the format: <TelegramID> <Amount>"
            )
            return ADMIN_CREDIT

    return ConversationHandler.END


async def handle_admin_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id, amount = map(int, update.message.text.split())
        target_user = get_user_by_telegram_id(user_id)

        if not target_user:
            await update.message.reply_text("Usuário não encontrado.")
            return ConversationHandler.END

        target_user = update_user_credits(
            target_user, target_user.credit_balance + amount
        )

        await update.message.reply_text(
            f"Créditos adicionados!\n{target_user.name}: {target_user.credit_balance}"
        )

        await context.bot.send_message(
            chat_id=target_user.telegram_id,
            text=get_text("pt_BR", "messages.credits.gift").format(
                amount=amount, user_balance=target_user.credit_balance
            ),
        )
        await context.bot.send_message(
            chat_id=target_user.telegram_id,
            text=get_text("pt_BR", "messages.menu").format(
                user_balance=target_user.credit_balance if target_user else 0,
                value_description=VALUE_DESCRIPTION,
                value_audio=VALUE_AUDIO_TRANSCRIPTION,
            ),
        )

    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

    return ConversationHandler.END
