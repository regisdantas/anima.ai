import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    Defaults,
    MessageHandler,
    filters
)

from handlers.start import handle_start, handle_help
from handlers.credits import handle_credits, handle_payments
from handlers.history import handle_history
from handlers.customization import handle_customize
from handlers.terms import handle_terms, handle_accept_terms, handle_decline_terms
from handlers.user_message import handle_user_message

class AnimaAITelegramBot:
    def __init__(self, token: str):
        if not token:
            raise ValueError("Telegram bot Token was not provided.")

        self.token = token

        with open("app/bot/lang/pt_BR.json", "r") as file:
            self.messages = json.load(file)

        df = Defaults(block=False)
        self.app = Application.builder().token(self.token).connect_timeout(30).defaults(df).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler(self.messages["commands"]["start"], handle_start))
        self.app.add_handler(CommandHandler(self.messages["commands"]["help"], handle_help))
        self.app.add_handler(CommandHandler(self.messages["commands"]["credits"], handle_credits))
        self.app.add_handler(CommandHandler(self.messages["commands"]["payments"], handle_payments))
        self.app.add_handler(CommandHandler(self.messages["commands"]["history"], handle_history))
        self.app.add_handler(CommandHandler(self.messages["commands"]["customize"], handle_customize))
        self.app.add_handler(CommandHandler(self.messages["commands"]["terms"], handle_terms))
        self.app.add_handler(CommandHandler(self.messages["commands"]["accept_terms"], handle_accept_terms))
        self.app.add_handler(CommandHandler(self.messages["commands"]["decline_terms"], handle_decline_terms))

        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    
    def start(self):
        self.app.run_polling()

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = AnimaAITelegramBot(token=token)
    bot.start()