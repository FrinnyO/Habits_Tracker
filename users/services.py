import requests
from django.conf import settings


def get_tg_chat_id():
    response = requests.get(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates",
    )
    try:
        chat_id = response.json()["result"][0]["message"]["chat"]["id"]
        return chat_id
    except (KeyError, IndexError) as e:
        return None
