"""This module contains all the constants used in the application."""

# Standard library imports
import os

# Third party imports
from dotenv import load_dotenv

load_dotenv()

# Tokens
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

# Model Constants
TEMPERATURE: float = 0.7
TEMPLATE: list = []
WHISPER_MODEL = "whisper-1"
GPT3_MODEL: str = "gpt-3.5-turbo"
GPT4_MODEL: str = "gpt-4"

# HTTP Constants
HTTP_OK = 200
