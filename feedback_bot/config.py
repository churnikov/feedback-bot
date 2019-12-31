import os
from pathlib import Path

from feedback_bot.command_replies import Replies

TG_TOKEN = os.environ["TG_BOT_TOKEN"]
PROXY = os.environ.get("RT_HTTPS_PROXY")
CHAT_ID = int(os.environ["TG_CHAT_ID"])
REPLIES: Replies = Replies.load_from_dir(Path(os.environ["COMMAND_REPLIES_PATH"]))
BOT_TIMEOUT = int(os.environ.get("BOT_TIMEOUT", 10))
BOT_RETRIES = int(os.environ.get("BOT_RETRIES", 5))
