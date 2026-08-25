"""
Точка входа. Запускается командой: python main.py

Что происходит при запуске:
1. Создаём объект бота с токеном из .env
2. Создаём диспетчер (он распределяет входящие сообщения по хендлерам)
3. Подключаем все роутеры из handlers/
4. Запускаем polling — бот начинает опрашивать Telegram на новые сообщения
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import all_routers

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # MemoryStorage хранит состояния FSM в оперативной памяти.
    # Если бот перезапустится — все "незавершённые" заказы сбросятся.
    # Для продакшна можно заменить на RedisStorage, но для MVP этого достаточно.
    dp = Dispatcher(storage=MemoryStorage())

    for router in all_routers:
        dp.include_router(router)

    # Сбрасываем накопленные обновления, чтобы при старте бот не отвечал
    # на старые сообщения, пришедшие пока бот был выключен
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
