"""This module contains the main function for the telegram_bot."""

import os
from dotenv import load_dotenv
import logging
import tempfile
# import pickle
from gtts import gTTS
from telegram import Update, InputFile, File, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import requests
import json

import openai
from pydub import AudioSegment
from io import BytesIO

from langdetect import detect

from functools import wraps
import threading
import time

class TypingThread(threading.Thread):
    def __init__(self, chat_id, bot, action):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot
        self.action = action
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            self.bot.send_chat_action(chat_id=self.chat_id, action=self.action)
            time.sleep(0.5)

    def stop(self):
        self._stop_event.set()

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            typing_thread = TypingThread(update.effective_chat.id, context.bot, action)
            typing_thread.start()

            # Ejecuta la función del handler
            res = func(update, context)

            # Detiene el hilo de la acción de chat "escribiendo..."
            typing_thread.stop()
            typing_thread.join()
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
GPT3_MODEL: str = "gpt-3.5-turbo"
GPT4_MODEL: str = "gpt-4"

def gpt_request(text: str, messages: list, model: str) -> str:
    """Ask something to GPT-3.5 Turbo."""
    if not text:
        return "empty message"
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_TOKEN
    }
    messages.append({'role': 'user', 'content': text})
    # messages.append({'role': 'user', 'content': text})
    data = {
        'model': model,
        'messages': messages,
        'temperature': TEMPERATURE,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200 or "choices" not in response.json():
        return response.text
    content = response.json()['choices'][0]['message']['content']
    messages.append({'role': 'assistant', 'content': content})
    # messages.append({'role': 'assistant', 'content': content})
    return content

def audio_to_text(audio: File) -> str:
    """Convert audio to text."""
    # Descargar el archivo de audio en un objeto BytesIO
    audio_data = BytesIO()
    audio.download(out=audio_data)
    audio_data.seek(0)

    # Convertir el archivo de audio a formato WAV
    audio_segment = AudioSegment.from_ogg(audio_data)
    wav_data = BytesIO()
    audio_segment.export(wav_data, format='wav')
    wav_data.seek(0)

    # Asignar un nombre arbitrario al objeto BytesIO
    wav_data.name = "temp_audio.wav"

    # Cargar el objeto BytesIO directamente en la función de transcripción
    transcript = openai.Audio.transcribe("whisper-1", wav_data)['text']

    return transcript

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
def get_text_from_text(update: Update, context: CallbackContext) -> None:
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = gpt_request(
                        update.message.text, \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    return response

@send_record_voice_action
def get_audio_from_text(update: Update, context: CallbackContext) -> None:
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = gpt_request(
                        update.message.text, \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    language: str = detect(response)
    # Convertir texto a audio usando gTTS y la función convert_text_to_audio
    audio_file_path = text_to_audio(response, language)
    return audio_file_path

@send_typing_action
def get_text_from_audio(update: Update, context: CallbackContext) -> None:
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = gpt_request(
                        audio_to_text(context.bot.getFile(update.message.voice.file_id)), \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    return response

@send_record_voice_action
def get_audio_from_audio(update: Update, context: CallbackContext) -> None:
    if "messages" not in context.user_data:
        context.user_data['messages'] = TEMPLATE.copy()
    response: str = gpt_request(
                        audio_to_text(context.bot.getFile(update.message.voice.file_id)), \
                        context.user_data['messages'], \
                        context.user_data.get("model", GPT3_MODEL)
                    )
    language: str = detect(response)
    # Convertir texto a audio usando gTTS y la función convert_text_to_audio
    audio_file_path = text_to_audio(response, language)
    return audio_file_path

def handle_text(update: Update, context: CallbackContext) -> None:
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        # Convertir texto a audio usando gTTS y la función convert_text_to_audio
        audio_file_path = get_audio_from_text(update, context)

        # Enviar audio como respuesta
        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file), \
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            get_text_from_text(update, context), \
            reply_to_message_id = update.message.message_id
        )

def handle_audio(update: Update, context: CallbackContext) -> None:
    if "send_audio" in context.user_data and context.user_data['send_audio']:
        # Convertir texto a audio usando gTTS y la función convert_text_to_audio
        audio_file_path = get_audio_from_audio(update, context)

        # Enviar audio como respuesta
        with open(audio_file_path, "rb") as audio_file:
            update.message.reply_voice(
                voice=InputFile(audio_file), \
                reply_to_message_id=update.message.message_id
            )
    else:
        update.message.reply_text(
            get_text_from_audio(update, context), \
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
