from loguru import logger
from telegram import Message, Update
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


def forward_callback(update: Update, context: CallbackContext):
    """Forward the user message to ``CHAT_ID``."""
    message: Message = update.message
    message.forward(CHAT_ID)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "{}" caused error "{}"', update, context.error)
