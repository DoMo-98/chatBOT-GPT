"""This module contains the commands for the telegram_bot."""

# Third party imports
from telegram import Update
from telegram.ext import CallbackContext

# Local application imports
from src.constants import (GPT3_MODEL, GPT4_MODEL, TEMPLATE)


HELP_MESSAGE = '''
/start - Initialize the bot
/text - Switch to text mode
/audio - Switch to audio mode
/new - Start a new chat
/gpt3 - Switch to GPT-3.5-Turbo
/gpt4 - Switch to GPT-4
'''

def help_command(update: Update, context: CallbackContext) -> None:
    """
    Respond to the /help command.
    Send a message detailing the available commands and their function.
    """
    update.message.reply_text(HELP_MESSAGE)

def start_command(update: Update, context: CallbackContext) -> None:
    """Initialize the bot when the command /start is issued."""
    context.user_data['messages'] = TEMPLATE.copy()
    update.message.reply_text("Hello! I'm an assistant bot. I can answer all your text and voice messages.")

def text_command(update: Update, context: CallbackContext):
    """Switch the bot to text mode when the command /text is issued."""
    context.user_data['send_audio'] = False
    update.message.reply_text("I will now send text messages.")

def audio_command(update: Update, context: CallbackContext):
    """Switch the bot to audio mode when the command /audio is issued."""
    context.user_data['send_audio'] = True
    update.message.reply_text("I will now send voice messages.")

def new_chat_command(update: Update, context: CallbackContext) -> None:
    """Start a new chat when the command /new is issued."""
    context.user_data['messages'] = TEMPLATE.copy()
    update.message.reply_text("New chat!")

def gpt_3_command(update: Update, context: CallbackContext) -> None:
    """Switch the bot to use GPT-3.5-Turbo when the command /gpt3 is issued."""
    context.user_data['model'] = GPT3_MODEL
    update.message.reply_text("I will now use GPT-3.5-Turbo.")

def gpt_4_command(update: Update, context: CallbackContext) -> None:
    """Switch the bot to use GPT-4 when the command /gpt4 is issued."""
    context.user_data['model'] = GPT4_MODEL
    update.message.reply_text("I will now use GPT-4.")
