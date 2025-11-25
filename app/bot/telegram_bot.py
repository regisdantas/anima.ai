import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    Defaults,
)

from handlers.start import start, help
from handlers.credits import credits, payments
from handlers.history import history
from handlers.customization import customize
from handlers.terms import terms, accept_terms, decline_terms

class AnimaAITelegramBot:
    def __init__(self, token: str):
        load_dotenv()
        self.token = token

        with open("app/bot/lang/pt_BR.json", "r") as file:
            self.messages = json.load(file)

        if not self.token:
            raise ValueError("Telegram bot Token was not provided.")
        df = Defaults(block=False)
        self.app = Application.builder().token(self.token).connect_timeout(30).defaults(df).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler(self.messages["commands"]["start"], start))
        self.app.add_handler(CommandHandler(self.messages["commands"]["help"], help))
        self.app.add_handler(CommandHandler(self.messages["commands"]["credits"], credits))
        self.app.add_handler(CommandHandler(self.messages["commands"]["payments"], payments))
        self.app.add_handler(CommandHandler(self.messages["commands"]["history"], history))
        self.app.add_handler(CommandHandler(self.messages["commands"]["customize"], customize))
        self.app.add_handler(CommandHandler(self.messages["commands"]["terms"], terms))
        self.app.add_handler(CommandHandler(self.messages["commands"]["accept_terms"], accept_terms))
        self.app.add_handler(CommandHandler(self.messages["commands"]["decline_terms"], decline_terms))
    
    def start(self):
        self.app.run_polling()

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = AnimaAITelegramBot(token=token)
    bot.start()