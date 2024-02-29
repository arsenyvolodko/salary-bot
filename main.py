import logging
import sys

from config import TOKEN
from aiogram import Bot
import asyncio

from src.bot.actions import dp


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
