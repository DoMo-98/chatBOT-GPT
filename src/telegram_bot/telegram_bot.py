"""This module contains the TelegramBot class."""

# Standard library imports
import logging

# Third party imports
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Local application imports
from src.telegram_bot.commands import (audio_command, gpt_3_command, gpt_4_command, help_command,
                                       new_chat_command, start_command, text_command)
from src.telegram_bot.handlers import handle_audio, handle_text


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
        self._dp.add_handler(CommandHandler("help", help_command))
        self._dp.add_handler(CommandHandler("start", start_command))
        self._dp.add_handler(CommandHandler("text", text_command))
        self._dp.add_handler(CommandHandler("audio", audio_command))
        self._dp.add_handler(CommandHandler("new", new_chat_command))
        self._dp.add_handler(CommandHandler("gpt3", gpt_3_command))
        self._dp.add_handler(CommandHandler("gpt4", gpt_4_command))
        self._dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
        self._dp.add_handler(MessageHandler(Filters.voice | Filters.audio, handle_audio))

    def run(self):
        """Start the bot."""
        self.updater.start_polling()
        self.updater.idle()
