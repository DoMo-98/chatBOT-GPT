"""This module contains the Telegram bot handlers."""

# Standard library imports
import asyncio

# Third party imports
from telegram import InputFile, Update
from telegram.ext import CallbackContext

# Local application imports
from constants import TEMPLATE
from telegram_bot.chat_interactions import (get_audio_from_audio, get_audio_from_text,
                                           get_text_from_audio, get_text_from_text)


def handle_text(update: Update, context: CallbackContext) -> None:
    """Send a message when receiving a text message."""
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        audio_file_path = asyncio.run( get_audio_from_text(update, context) )

        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file),
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            asyncio.run( get_text_from_text(update, context) ),
            reply_to_message_id = update.message.message_id
        )

def handle_audio(update: Update, context: CallbackContext) -> None:
    """Send a message when receiving an audio or voice message."""
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        audio_file_path = asyncio.run( get_audio_from_audio(update, context) )

        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file),
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            asyncio.run( get_text_from_audio(update, context) ),
            reply_to_message_id = update.message.message_id
        )

# def handle_update(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     if "messages" not in context.user_data:
#         context.user_data['messages'] = TEMPLATE.copy()
#     if "send_audio" not in context.user_data:
#         context.user_data['send_audio'] = False
#     return False
