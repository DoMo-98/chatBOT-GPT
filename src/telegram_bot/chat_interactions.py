"""This module contains functions for interaction with OpenAI API."""

# Third party imports
from langdetect import detect
from telegram import Update
from telegram.ext import CallbackContext

# Local application imports
from constants import GPT3_MODEL, TEMPLATE
from openai_api.gpt_request import gpt_request
from helpers.audio_to_text import audio_to_text
from helpers.text_to_audio import text_to_audio
from telegram_bot.decorators.send_action import send_record_voice_action, send_typing_action


async def sample_gpt_request(text: str, context: CallbackContext):
    """Send a request to OpenAI API and get a response."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    return await gpt_request(
        text,
        context.user_data['messages'],
        context.user_data.get("model", GPT3_MODEL)
    )

@send_typing_action
async def get_text_from_text(update: Update, context: CallbackContext) -> str:
    """Send a request to OpenAI API and get a response."""
    response: str = await sample_gpt_request(update.message.text, context)
    return response

@send_record_voice_action
async def get_audio_from_text(update: Update, context: CallbackContext) -> str:
    """Send a request to OpenAI API, get a response and convert it to audio."""
    response: str = await sample_gpt_request(update.message.text, context)
    language: str = detect(response)
    audio_file_path = text_to_audio(response, language)
    return audio_file_path

@send_typing_action
async def get_text_from_audio(update: Update, context: CallbackContext) -> str:
    """Convert audio to text, send a request to OpenAI API and get a response."""
    text: str = await audio_to_text(context.bot.getFile(update.message.voice.file_id))
    response: str = await sample_gpt_request(text, context)
    return response

@send_record_voice_action
async def get_audio_from_audio(update: Update, context: CallbackContext) -> str:
    """Convert audio to text, send a request to OpenAI API, get a response and convert it to audio."""
    text: str = await audio_to_text(context.bot.getFile(update.message.voice.file_id))
    response: str = await sample_gpt_request(text, context)
    language: str = detect(response)
    audio_file_path = text_to_audio(response, language)
    return audio_file_path
