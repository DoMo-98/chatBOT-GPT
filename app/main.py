"""This module contains the main function for the telegram_bot."""

# Standard library imports
import asyncio
import json
import logging
import os
import tempfile
# import pickle
from functools import wraps
from io import BytesIO

# Third party imports
import aiohttp
import openai
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
from telegram import ChatAction, File, InputFile, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater


async def typing(chat_id, bot, action):
    """Sends `action` while processing func command."""
    while True:
        bot.send_chat_action(chat_id=chat_id, action=action)
        await asyncio.sleep(1)

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            typing_task = asyncio.create_task(typing(update.effective_chat.id, context.bot, action))

            res = await func(update, context)

            typing_task.cancel()
            try:
                await typing_task
            except asyncio.CancelledError:
                logging.info("typing_task cancelled")
            return res
        return command_func

    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_record_voice_action = send_action(ChatAction.RECORD_VOICE)

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_API_KEY")
DEEPL_TOKEN: str = os.getenv("DEEPL_API_KEY")
OPENAI_TOKEN: str = os.getenv("OPENAI_API_KEY")

TEMPERATURE: float = 0.7
TEMPLATE: list = []
WHISPER_MODEL = "whisper-1"
GPT3_MODEL: str = "gpt-3.5-turbo"
GPT4_MODEL: str = "gpt-4"

async def gpt_request(text: str, messages: list, model: str) -> str:
    """Ask something to GPT-3.5 Turbo."""
    if not text:
        return "empty message"
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_TOKEN
    }
    messages.append({'role': 'user', 'content': text})
    data = {
        'model': model,
        'messages': messages,
        'temperature': TEMPERATURE,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            response_data = await response.text()
            if response.status != 200:
                return response_data
            response_json = await response.json()
            if "choices" not in response_json:
                return response_data
            content = response_json['choices'][0]['message']['content']
            messages.append({'role': 'assistant', 'content': content})
            return content

async def audio_to_text(audio: File) -> str:
    """Convert audio to text."""
    # Download the audio file
    audio_data = BytesIO()
    audio.download(out=audio_data)
    audio_data.seek(0)

    # Convert the audio file to wav
    audio_segment = AudioSegment.from_ogg(audio_data)
    wav_data = BytesIO()
    audio_segment.export(wav_data, format='wav')
    wav_data.seek(0)

    # Asign a name to the BytesIO object
    wav_data.name = "temp_audio.wav"

    # Load the BytesIO object directly into the atranscribe function
    openai.api_key = OPENAI_TOKEN
    transcript = await openai.Audio.atranscribe(WHISPER_MODEL, wav_data)

    return transcript['text']

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

def handle_text(update: Update, context: CallbackContext) -> None:
    """Send a message when receiving a text message."""
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        audio_file_path = asyncio.run( get_audio_from_text(update, context) )

        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file), \
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            asyncio.run( get_text_from_text(update, context) ), \
            reply_to_message_id = update.message.message_id
        )

def handle_audio(update: Update, context: CallbackContext) -> None:
    """Send a message when receiving an audio or voice message."""
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        audio_file_path = asyncio.run( get_audio_from_audio(update, context) )

        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file), \
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            asyncio.run( get_text_from_audio(update, context) ), \
            reply_to_message_id = update.message.message_id
        )

def handle_update(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    if "send_audio" not in context.user_data:
        context.user_data['send_audio'] = False
    return False

def text_to_audio(text: str, lang="es") -> str:
    """Convert text to audio using gTTS."""
    tts = gTTS(text, lang=lang)
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".ogg", delete=False) as _f:
        tts.save(_f.name)
    return _f.name

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
