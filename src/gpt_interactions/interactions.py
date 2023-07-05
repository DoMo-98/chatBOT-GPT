"""This module contains functions for interaction with OpenAI API."""

# Third party imports
from langdetect import detect
from telegram import Update
from telegram.ext import CallbackContext

# Local application imports
from constants import GPT3_MODEL, TEMPLATE
from telegram_bot.decorators.send_action import send_record_voice_action, send_typing_action
from gpt_interactions.helpers import audio_to_text, gpt_request, text_to_audio

@send_typing_action
async def get_text_from_text(update: Update, context: CallbackContext) -> None:
    """Send a request to OpenAI API and get a response."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = await gpt_request(
                        update.message.text, \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    return response

@send_record_voice_action
async def get_audio_from_text(update: Update, context: CallbackContext) -> None:
    """Send a request to OpenAI API, get a response and convert it to audio."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = await gpt_request(
                        update.message.text, \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    language: str = detect(response)
    audio_file_path = text_to_audio(response, language)
    return audio_file_path

@send_typing_action
async def get_text_from_audio(update: Update, context: CallbackContext) -> None:
    """Convert audio to text, send a request to OpenAI API and get a response."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = await gpt_request(
                        await audio_to_text(context.bot.getFile(update.message.voice.file_id)), \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    return response

@send_record_voice_action
async def get_audio_from_audio(update: Update, context: CallbackContext) -> None:
    """Convert audio to text, send a request to OpenAI API, get a response and convert it to audio."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = await gpt_request(
                        await audio_to_text(context.bot.getFile(update.message.voice.file_id)), \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    language: str = detect(response)
    audio_file_path = text_to_audio(response, language)
    return audio_file_path
