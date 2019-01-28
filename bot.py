from telegram.ext import Filters
from telegram.ext import Updater, CommandHandler, MessageHandler

import config
from filters import SpecificTextHandler
from handlers import start, error, refresh_handler, vote_handler


def setup_bot(handlers, error_handler=None):
    updater = Updater(config.TELEGRAM_BOT_TOKEN, request_kwargs=config.TELEGRAM_PROXY_CONFIG)
    dp = updater.dispatcher
    for handler in handlers:
        dp.add_handler(handler)
    if error_handler:
        dp.add_error_handler(error_handler)
    return updater


def start_bot(bot):
    bot.start_polling(timeout=config.POLLING_TIMEOUT_SEC)
    bot.idle()


if __name__ == '__main__':
    bot = setup_bot(
        handlers=[
            CommandHandler("start", start),
            MessageHandler(SpecificTextHandler(config.REFRESH_BUTTON_TEXT), refresh_handler),
            MessageHandler(Filters.text, vote_handler),
        ],
        error_handler=error,
    )
    start_bot(bot)
