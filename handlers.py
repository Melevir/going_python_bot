import logging

from telegram import ReplyKeyboardMarkup

import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет! Через меня можно голосовать во время доклада Ильи.',
        reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
    )


def refresh_handler(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"', update, error)