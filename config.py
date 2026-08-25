"""
Конфигурация бота.
Все секреты (токен, id админа) хранятся в .env, а не в коде —
это нужно, чтобы случайно не запушить токен в публичный репозиторий.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN не найден. Скопируй .env.example в .env и впиши туда токен от @BotFather."
    )

if not ADMIN_CHAT_ID:
    raise ValueError(
        "ADMIN_CHAT_ID не найден. Узнай свой id через @userinfobot и впиши его в .env."
    )
