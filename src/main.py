"""This module contains the main function for the telegram_bot."""

# Standard library imports
import logging

# Third party imports
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Local application imports
from constants import TELEGRAM_TOKEN
from telegram_bot.commands import audio, gpt_3, gpt_4, new_chat, start, text
from telegram_bot.handlers import handle_audio, handle_text


def main():
    """Start the bot."""
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                        level=logging.INFO)
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    _dp = updater.dispatcher

    # _dp.add_handler(MessageHandler(Filters.all, handle_update, run_async=True))
    _dp.add_handler(CommandHandler("start", start))
    _dp.add_handler(CommandHandler("text", text))
    _dp.add_handler(CommandHandler("audio", audio))
    _dp.add_handler(CommandHandler("new", new_chat))
    _dp.add_handler(CommandHandler("gpt3", gpt_3))
    _dp.add_handler(CommandHandler("gpt4", gpt_4))
    _dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    _dp.add_handler(MessageHandler(Filters.voice | Filters.audio, handle_audio))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
