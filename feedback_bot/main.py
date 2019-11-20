# Start the bot
# Create the Updater and pass it your bot's token.
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from feedback_bot.bot import error, forward_and_reply_callback, help_callback, start_callback
from feedback_bot.config import TG_TOKEN

updater = Updater(TG_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start_callback))
dp.add_handler(CommandHandler("help", help_callback))

# Messages handler
dp.add_handler(MessageHandler(Filters.all, forward_and_reply_callback))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

updater.idle()
