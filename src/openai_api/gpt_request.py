"""This module contains gpt_request function for the app."""

# Standard library imports
import json

# Third party imports
import aiohttp

# Local application imports
from src.constants import (OPENAI_API_KEY, TEMPERATURE, HTTP_OK)


async def construct_request_payload(text: str, messages: list, model: str) -> dict:
    """Construct the request payload for the GPT request."""
    messages.append({'role': 'user', 'content': text})
    data = {
        'model': model,
        'messages': messages,
        'temperature': TEMPERATURE,
    }
    return data

async def send_gpt_request(session: aiohttp.ClientSession, url: str, headers: dict, data: dict) -> dict:
    """Send the request to the GPT API and return the response."""
    async with session.post(url, headers=headers, data=json.dumps(data)) as response:
        response_data = await response.text()
        if response.status != HTTP_OK:
            return response_data
        response_json = await response.json()
        return response_json

async def extract_content_from_response(response_json: dict, messages: list) -> str:
    """Extract the content from the response JSON."""
    if "choices" not in response_json:
        return response_json
    content = response_json['choices'][0]['message']['content']
    messages.append({'role': 'assistant', 'content': content})
    return content

async def gpt_request(text: str, messages: list, model: str) -> str:
    """Send a request to the OpenAI Model API."""
    if not text:
        return "empty message"
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY
    }

    data = await construct_request_payload(text, messages, model)

    async with aiohttp.ClientSession() as session:
        response_json = await send_gpt_request(session, url, headers, data)

    content = await extract_content_from_response(response_json, messages)

    return content
