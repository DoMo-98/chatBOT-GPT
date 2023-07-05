"""This module contains the send_action decorator for the telegram_bot."""

# Standard library imports
import asyncio
import logging
from functools import wraps

# Third party imports
from telegram import ChatAction


async def _loop_action(chat_id, bot, action):
    """Sends `action` in a loop until cancelled."""
    while True:
        bot.send_chat_action(chat_id=chat_id, action=action)
        await asyncio.sleep(1)

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context):
            loop_action_task = asyncio.create_task(
                _loop_action(
                    update.effective_chat.id,
                    context.bot,
                    action
                )
            )

            res = await func(update, context)

            loop_action_task.cancel()
            try:
                await loop_action_task
            except asyncio.CancelledError:
                logging.info("loop_action_task cancelled")
            return res
        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_record_voice_action = send_action(ChatAction.RECORD_VOICE)
