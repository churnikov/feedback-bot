# Start the bot
# Create the Updater and pass it your bot's token.
from telegram.ext import CommandHandler, filters, MessageHandler, Application

from feedback_bot.bot import error, forward_callback, help_callback, reply_callback, start_callback
from feedback_bot.config import TG_TOKEN


def main():
    app = Application.builder().token(
        token=TG_TOKEN,
    )

    # Get the dispatcher to register handlers
    dp = app.build()

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_callback))
    dp.add_handler(CommandHandler("help", help_callback))

    # Messages handler
    dp.add_handler(MessageHandler(filters.REPLY, reply_callback))
    dp.add_handler(MessageHandler(filters.ALL, forward_callback))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    dp.run_polling()



if __name__ == "__main__":
    main()
