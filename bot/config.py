import os


TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

TELEGRAM_PROXY_CONFIG = {
    'proxy_url': os.environ.get('TELEGRAM_PROXY_URL'),
    'urllib3_proxy_kwargs': {
        'username': os.environ.get('TELEGRAM_PROXY_LOGIN'),
        'password': os.environ.get('TELEGRAM_PROXY_PASSWORD'),
    },
}

POLLING_TIMEOUT_SEC = 2


REFRESH_BUTTON_TEXT = 'Показать активный вопрос'
