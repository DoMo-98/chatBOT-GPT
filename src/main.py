"""This module contains the main function for the telegram_bot."""

# Local application imports
from constants import TELEGRAM_TOKEN
from telegram_bot.telegram_bot import TelegramBot


if __name__ == "__main__":
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.run()
