from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from settings import Settings

from routers import main, scenes
from routers.scenes import *


def create_dispatcher(settings: Settings) -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        settings=settings,
        events_isolation=SimpleEventIsolation(),
    )
    dispatcher.include_routers(main.router, scenes.router)
    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(add_book.Add_book, title_book.Title_book, description_book.Description_book, author_book.Author_book, genre_book.Genre_book, all_books.All_books, search.Search)
    return dispatcher


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML
    )
