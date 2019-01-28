import logging

from telegram import ReplyKeyboardMarkup

import config
from api import fetch_active_question_info, save_vote_to_api

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


ACTIVE_QUESTION_INFO = None  # текущий активный вопрос, один на всех
VOTED_INFO = set()  # информация о том, кто из пользователей проголосовал за какой из вопросов


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет! Через меня можно голосовать во время доклада Ильи.',
        reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
    )


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"', update, error)


def refresh_handler(bot, update):
    active_question = fetch_active_question_info(add_random_emoji=True)
    global ACTIVE_QUESTION_INFO
    ACTIVE_QUESTION_INFO = active_question
    if (update.message.chat.username, ACTIVE_QUESTION_INFO['question_id']) in VOTED_INFO:
        # пользователь уже проголосовал за активный вопрос
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Вы уже проголосовали за активный вопрос, давайте ждать следующего вопроса.',
            reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
        )
        return

    buttons = [[c['text']] for c in active_question['options']]
    bot.send_message(
        chat_id=update.message.chat_id,
        text=active_question['question_text'],
        reply_markup=ReplyKeyboardMarkup(buttons),
    )


def vote_handler(bot, update):
    selected_option_text = update.message.text
    option_id = [o['id'] for o in ACTIVE_QUESTION_INFO['options'] if o['text'] == selected_option_text]
    if not option_id:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Это не ответ на активный вопрос. Вы хотите поболтать? Приходите в чатик Pyladies!',
            reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
        )
        return
    option_id = option_id[0]
    if (update.message.chat.username, option_id) in VOTED_INFO:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Вы уже ответили на этот вопрос.',
            reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
        )

    save_vote_to_api(ACTIVE_QUESTION_INFO['question_id'], option_id, update.message.chat.username)
    VOTED_INFO.add(
        (update.message.chat.username, ACTIVE_QUESTION_INFO['question_id']),
    )
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Спасибо, мы записали.',
        reply_markup=ReplyKeyboardMarkup([[config.REFRESH_BUTTON_TEXT]]),
    )
