import json
from typing import List, Optional, Union

from loguru import logger
from telegram import Message, TelegramObject, Update
from telegram.ext import CallbackContext

from feedback_bot.config import BOT_RETRIES, BOT_TIMEOUT, CHAT_ID, REPLIES
from feedback_bot.retry import TelegramTimedOutRetry


async def start_callback(update: Update, context: CallbackContext):
    """Send a message when the command ``/start`` is issued."""
    message = update.message
    await message.reply_markdown(REPLIES.start)


async def help_callback(update: Update, context: CallbackContext):
    """Send a message when the command ``/help`` is issued."""
    message = update.message
    await message.reply_markdown(REPLIES.help)


def prepare_params(attachment: TelegramObject, at: str, reply_to_id: int) -> Optional[dict]:
    """prepare params for bots' ``send_*``."""
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

    return params


async def reply_callback(update: Update, context: CallbackContext):
    message: Message = update.message
    logger.info(message)

    if message.chat_id == CHAT_ID:
        reply_to_id = message.reply_to_message.from_user.id
        reply_to_message_id = message.reply_to_message.message_id
        if message.text is not None:
            await TelegramTimedOutRetry(
                retry_count=BOT_RETRIES,
                function=context.bot.send_message,
                function_kwargs={
                    "chat_id": reply_to_id,
                    "text": message.text,
                    "reply_to_message_id": reply_to_message_id,
                    "pool_timeout": BOT_TIMEOUT,
                },
            ).retry()
        if message.effective_attachment is not None:
            for at in message.ATTACHMENT_TYPES:
                attachment: Union[TelegramObject, List[TelegramObject]] = getattr(message, at)
                if attachment is not None:

                    params = prepare_params(attachment, at, reply_to_id)
                    if params is None:
                        continue

                    params["pool_timeout"] = BOT_TIMEOUT
                    await TelegramTimedOutRetry(
                        retry_count=BOT_RETRIES,
                        function=getattr(context.bot, f"send_{at}"),
                        function_kwargs=params,
                    ).retry()

                    break
    else:
        await TelegramTimedOutRetry(
            retry_count=BOT_RETRIES,
            function=context.bot.forward_message,
            function_kwargs={
                "chat_id": CHAT_ID,
                "reply_to_message_id": message.message_id,
                "pool_timeout": BOT_TIMEOUT,
            },
        ).retry()


async def forward_callback(update: Update, context: CallbackContext):
    """Forward the user message to ``CHAT_ID``."""
    message: Message = update.message

    logger.info(message)

    await TelegramTimedOutRetry(
        retry_count=BOT_RETRIES,
        function=context.bot.forward_message,
        function_kwargs={
            "chat_id": CHAT_ID,
            "from_chat_id": message.chat_id,
            "message_id": message.message_id,
            "pool_timeout": BOT_TIMEOUT,
        },
    ).retry()


async def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "{}" caused error "{}"', update, context.error)
