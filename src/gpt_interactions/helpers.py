"""This module contains helper functions for the app."""

# Standard library imports
import json
import tempfile
from io import BytesIO

# Third party imports
import aiohttp
import openai
from gtts import gTTS
from pydub import AudioSegment
from telegram import File

# Local application imports
from constants import (OPENAI_TOKEN, TEMPERATURE, WHISPER_MODEL)


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

def text_to_audio(text: str, lang="es") -> str:
    """Convert text to audio using gTTS."""
    tts = gTTS(text, lang=lang)
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".ogg", delete=False) as _f:
        tts.save(_f.name)
    return _f.name
