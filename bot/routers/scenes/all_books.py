from typing import Final

from aiogram import F, Router
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.fabrics.fabrics import ButtonsCB, CheckBookCB, PaginationCB, Action
from bot.routers.main import start
from bot.database import base

from math import ceil

router: Final[Router] = Router(name=__name__)


class All_books(Scene, state="all_books"):
    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery):
        all_books = base.Book.select().limit(5)
        books_quantity = len(all_books)
        keyboard: list[InlineKeyboardButton] = []

        pagination: InlineKeyboardBuilder = InlineKeyboardBuilder()

        for book in all_books:
            keyboard.append(InlineKeyboardButton(text=book.name, callback_data=CheckBookCB(action='check_book', book=book.id).pack()))

        pagination.row(*keyboard)
        pagination.row(InlineKeyboardButton(text='Назад', callback_data=ButtonsCB(action=Action.BACK).pack()),
                       InlineKeyboardButton(text='▶️', callback_data=PaginationCB(action='page', offset=books_quantity, page=1).pack()))

        await callback.message.edit_text(text='Выбери фильм о котором хочешь узнать побольше!',
                                         reply_markup=pagination.as_markup())

    @on.callback_query(ButtonsCB.filter(F.action == Action.BACK), after=After.exit())
    async def back(self, _: CallbackQuery) -> None:
        await start.start_command_back(_)
        pass

    @on.callback_query(PaginationCB.filter(F.action == "page"))
    async def page(self, callback: CallbackQuery, callback_data: PaginationCB):
        if callback_data.page >= 0:
            previous_page = callback_data.page - 1
            next_page = callback_data.page + 1
            books_per_page = 5

            books = base.Book.select().offset(callback_data.page * books_per_page)
            books_limit = books.limit(books_per_page)
            books_quantity = len(books_limit)

            pagination: InlineKeyboardBuilder = InlineKeyboardBuilder()
            keyboard: list[InlineKeyboardButton] = []

            for book in books_limit:
                keyboard.append(InlineKeyboardButton(text=book.name, callback_data=CheckBookCB(action='check_book', book=book.id).pack()))

            pagination.row(*keyboard)

            pagination.row(InlineKeyboardButton(text='◀️', callback_data=PaginationCB(action='page', offset=previous_page * books_per_page, page=previous_page).pack()),
                           InlineKeyboardButton(text="↩️ Назад", callback_data=ButtonsCB(action=Action.BACK).pack()),
                           InlineKeyboardButton(text='▶️', callback_data=PaginationCB(action='page', offset=books_quantity, page=next_page).pack()), )

            await callback.message.edit_reply_markup(reply_markup=pagination.as_markup())
            return

    @on.callback_query(CheckBookCB.filter(F.action == "check_book"))
    async def check_book(self, callback: CallbackQuery, callback_data: CheckBookCB):
        book = base.Book.get(callback_data.book)

        await callback.message.answer(text=f'Название книги: {book.name}\n'
                                           f'Описание книги: {book.description}\n'
                                           f'Автор книги: {book.author}\n'
                                           f'Жанр книги: {book.genre}')
