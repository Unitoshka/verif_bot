import asyncio
import logging

from aiogram import Bot, Dispatcher

from factories import create_bot, create_dispatcher
from settings import Settings
from database import base


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    settings: Settings = Settings()
    dispatcher: Dispatcher = create_dispatcher(settings=settings)
    bot: Bot = create_bot(settings=settings)
    await dispatcher.start_polling(bot)
    return


if __name__ == '__main__':
    base.init()
    asyncio.run(main())
