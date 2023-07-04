"""This module contains the commands for the telegram_bot."""

# Third party imports
from telegram import Update
from telegram.ext import CallbackContext

# Local application imports
from constants import (GPT3_MODEL, GPT4_MODEL, TEMPLATE)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.user_data['messages'] = TEMPLATE.copy()
    update.message.reply_text("¡Hola! Soy un bot que recibe mensajes y audios.")

def text(update: Update, context: CallbackContext):
    """Send a message when the command /text is issued."""
    context.user_data['send_audio'] = False
    update.message.reply_text('Ahora enviaré mensajes de texto.')

def audio(update: Update, context: CallbackContext):
    """Send a message when the command /audio is issued."""
    context.user_data['send_audio'] = True
    update.message.reply_text('Ahora enviaré audios.')

def new_chat(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /new is issued."""
    context.user_data['messages'] = TEMPLATE.copy()
    update.message.reply_text("¡Nuevo chat!")

def gpt_3(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /gpt3 is issued."""
    context.user_data['model'] = GPT3_MODEL
    update.message.reply_text("Ahora usaré GPT-3.5-Turbo.")

def gpt_4(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /gpt4 is issued."""
    context.user_data['model'] = GPT4_MODEL
    update.message.reply_text("Ahora usaré GPT-4.")
