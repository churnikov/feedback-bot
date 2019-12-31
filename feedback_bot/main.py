# Start the bot
# Create the Updater and pass it your bot's token.
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from feedback_bot.bot import error, forward_callback, help_callback, reply_callback, start_callback
from feedback_bot.config import PROXY, TG_TOKEN


def main():
    updater = Updater(
        token=TG_TOKEN,
        use_context=True,
        request_kwargs={"proxy_url": PROXY} if PROXY is not None else None,
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_callback))
    dp.add_handler(CommandHandler("help", help_callback))

    # Messages handler
    dp.add_handler(MessageHandler(Filters.reply, reply_callback))
    dp.add_handler(MessageHandler(Filters.all, forward_callback))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
