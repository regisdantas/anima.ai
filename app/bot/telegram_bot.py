import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    Defaults,
)

class AnimaAITelegramBot:
    def __init__(self, token: str):
        load_dotenv()
        self.token = os.getenv("TELEGRAM_TOKEN") or token

        if not self.token:
            raise ValueError("TELEGRAM_TOKEN is not set in the .env file")
        df = Defaults(block=False)
        self.app = Application.builder().token(self.token).connect_timeout(30).defaults(df).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start_command)
        self.app.add_handler(start_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm Anima AI Telegram Bot.")

    def start(self):
        self.app.run_polling()

if __name__ == "__main__":
    bot = AnimaAITelegramBot(token="")
    bot.start()