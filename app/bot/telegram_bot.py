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

from app.bot.lang.lang_loader import get_language
from app.bot.handlers.start import handle_start, handle_help
from app.bot.handlers.credits import handle_credits, handle_payments
from app.bot.handlers.history import handle_history
from app.bot.handlers.customization import handle_customize
from app.bot.handlers.terms import handle_terms, handle_accept_terms, handle_decline_terms
from app.bot.handlers.user_message import handle_user_message



class AnimaAITelegramBot:
    def __init__(self, token: str):
        if not token:
            raise ValueError("Telegram bot Token was not provided.")
        self.language = get_language()
        df = Defaults(block=False)
        self.app = Application.builder().token(token).connect_timeout(30).defaults(df).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        print(self.language['commands'])
        self.app.add_handler(CommandHandler(self.language["commands"]["start"], handle_start))
        self.app.add_handler(CommandHandler(self.language["commands"]["help"], handle_help))
        self.app.add_handler(CommandHandler(self.language["commands"]["credits"], handle_credits))
        self.app.add_handler(CommandHandler(self.language["commands"]["payments"], handle_payments))
        self.app.add_handler(CommandHandler(self.language["commands"]["history"], handle_history))
        self.app.add_handler(CommandHandler(self.language["commands"]["customize"], handle_customize))
        self.app.add_handler(CommandHandler(self.language["commands"]["terms"], handle_terms))
        self.app.add_handler(CommandHandler(self.language["commands"]["accept_terms"], handle_accept_terms))
        self.app.add_handler(CommandHandler(self.language["commands"]["decline_terms"], handle_decline_terms))

        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    def start(self):
        self.app.run_polling()

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = AnimaAITelegramBot(token=token)
    bot.start()