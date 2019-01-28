from random import choice

from emoji import EMOJI_UNICODE


def fetch_active_question_info(add_random_emoji=False):
    question_info = {
        'question_text': 'Будешь учить английский?',
        'question_id': 32,
        'options': [
            {'id': 1, 'text': 'да'},
            {'id': 2, 'text': 'нет'},
        ],
    }
    if add_random_emoji:
        emojies = list(EMOJI_UNICODE.values())
        for option in question_info['options']:
            option['text'] = '{0} {1}'.format(
                choice(emojies),
                option['text'],
            )
    return question_info


def save_vote_to_api(question_id, option_id, user_id):
    print('Пользователь {0} выбрал вариант {1} на вопрос {2}'.format(  # noqa
        user_id,
        question_id,
        option_id,
    ))
