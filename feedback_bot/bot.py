import json
from typing import List, Optional, Union

from loguru import logger
from telegram import Message, TelegramObject, Update
from telegram.ext import CallbackContext

from feedback_bot.config import CHAT_ID, REPLIES


def start_callback(update: Update, context: CallbackContext):
    """Send a message when the command ``/start`` is issued."""
    message = update.message
    message.reply_markdown(REPLIES.start)


def help_callback(update: Update, context: CallbackContext):
    """Send a message when the command ``/help`` is issued."""
    message = update.message
    message.reply_markdown(REPLIES.help)


def prepare_params(
    attachment: TelegramObject, at: str, reply_to_id: int, reply_to_message_id: int
) -> Optional[dict]:
    if isinstance(attachment, list):
        if len(attachment) > 0:
            attachment = attachment[0]
        else:
            return None

    params = attachment.to_dict()

    logger.debug(json.dumps(params))

    file_id = params.pop("file_id", None)
    if file_id is not None:
        params[at] = file_id

    params["chat_id"] = reply_to_id
    params["reply_to_message_id"] = reply_to_message_id

    return params


def forward_and_reply_callback(update: Update, context: CallbackContext):
    """Forward the user message to ``CHAT_ID``."""
    message: Message = update.message
    reply_to_message: Optional[Message] = message.reply_to_message

    logger.info(message)

    if message.reply_to_message is not None and update.effective_chat.id == CHAT_ID:
        reply_to_id = reply_to_message.forward_from.id
        reply_to_message_id = reply_to_message.message_id - 1

        if message.text is not None:
            context.bot.send_message(
                chat_id=reply_to_id, text=message.text, reply_to_message_id=reply_to_message_id
            )
        if message.effective_attachment is not None:
            for at in message.ATTACHMENT_TYPES:
                attachment: Union[TelegramObject, List[TelegramObject]] = getattr(message, at)
                if attachment is not None:

                    params = prepare_params(attachment, at, reply_to_id, reply_to_message_id)
                    if params is None:
                        continue

                    getattr(context.bot, f"send_{at}")(**params)

                    break

    else:
        message.forward(CHAT_ID)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "{}" caused error "{}"', update, context.error)
