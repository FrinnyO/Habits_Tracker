import requests
from django.conf import settings


def send_tg_message(text, chat_id):
    params = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.get(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        params=params,
    )
