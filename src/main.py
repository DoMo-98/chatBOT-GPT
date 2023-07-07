"""This module contains the main function for the telegram_bot."""

# Local application imports
from constants import TELEGRAM_BOT_TOKEN
from telegram_bot.telegram_bot import TelegramBot


if __name__ == "__main__":
    bot = TelegramBot(TELEGRAM_BOT_TOKEN)
    bot.run()
