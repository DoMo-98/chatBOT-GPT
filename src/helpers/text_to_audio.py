"""This module contains the function for converting text to audio."""

# Standard library imports
import tempfile

# Third party imports
from gtts import gTTS


def text_to_audio(text: str, lang="es") -> str:
    """Convert text to audio using gTTS."""
    tts = gTTS(text, lang=lang)
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".ogg", delete=False) as _f:
        tts.save(_f.name)
    return _f.name
