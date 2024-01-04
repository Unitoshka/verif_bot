from typing import Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery

from bot.keyboards.base import create_keyboard, Keyboards
from bot.fabrics.fabrics import ButtonsCB, Action
from bot.routers.main import start
from bot.database import base

router: Final[Router] = Router(name=__name__)


class Add_book(Scene, state="add_book"):
    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        title, description, author, genre = (user_data.get('choosen_title', 'Отсутствует'),
                                             user_data.get('choosen_description', 'Отсутствует'),
                                             user_data.get('choosen_author', 'Отсутствует'),
                                             user_data.get('choosen_genre', 'Отсутствует'))

        await callback.message.edit_text(text="Начните добавлять книгу с того что вам будет удобным!\n\n"
                                              "Введенные вами данные:\n\n"
                                              f"Название книги: {title}\n"
                                              f"Описание книги: {description}\n"
                                              f"Автор: {author}\n"
                                              f"Жанр: {genre}",
                                         reply_markup=create_keyboard(Keyboards.CREATE_BOOK_KEYBOARD))

    @on.callback_query(ButtonsCB.filter(F.action == Action.BACK), after=After.exit())
    async def back(self, _: CallbackQuery) -> None:
        await start.start_command_back(_)

    @on.callback_query(F.data == 'finally_create')
    async def finally_create(self, callback: CallbackQuery, state: FSMContext) -> None:
        user_data = await state.get_data()
        title, description, author, genre = (user_data.get('choosen_title', None),
                                             user_data.get('choosen_description', None),
                                             user_data.get('choosen_author', None),
                                             user_data.get('choosen_genre', None))

        if title and description and author and genre:
            book = base.Book.get_or_create(name=title, description=description, author=author, genre=genre)

            await callback.message.edit_text(text='Книга была успешна добавлена!\n'
                                                  f'Её ID: {book[0]}')
            return

        await callback.message.edit_text(text='Похоже вы указали некорректные данные, попробуйте еще раз!')
