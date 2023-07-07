"""This module contains the TelegramBot class."""

# Standard library imports
import logging

# Third party imports
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Local application imports
from telegram_bot.commands import audio, gpt_3, gpt_4, new_chat, start, text
from telegram_bot.handlers import handle_audio, handle_text


class TelegramBot:
    """Telegram bot class."""
    def __init__(self, token):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.updater = Updater(token=token, use_context=True)
        self._dp = self.updater.dispatcher
        self.setup_handlers()

    def setup_handlers(self):
        """Setup the handlers for the bot."""
        self._dp.add_handler(CommandHandler("start", start))
        self._dp.add_handler(CommandHandler("text", text))
        self._dp.add_handler(CommandHandler("audio", audio))
        self._dp.add_handler(CommandHandler("new", new_chat))
        self._dp.add_handler(CommandHandler("gpt3", gpt_3))
        self._dp.add_handler(CommandHandler("gpt4", gpt_4))
        self._dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
        self._dp.add_handler(MessageHandler(Filters.voice | Filters.audio, handle_audio))

    def run(self):
        """Start the bot."""
        self.updater.start_polling()
        self.updater.idle()
