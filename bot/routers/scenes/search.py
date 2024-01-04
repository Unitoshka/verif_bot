from typing import Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.base import Keyboards
from bot.fabrics.fabrics import CheckBookCB
from bot.database import base

router: Final[Router] = Router(name=__name__)


class Search(Scene, state="search"):
    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery):
        await callback.message.answer(text="Введите ключевое слово для поиска\n"
                                           "(поиск производится лишь по автору и названию книги)")

    @on.message(F.text)
    async def search(self, message: Message):
        search = base.Book.select().where(base.Book.name.contains(message.text) | base.Book.author.contains(message.text))

        pagination: InlineKeyboardBuilder = InlineKeyboardBuilder()
        keyboard: list[InlineKeyboardButton] = []

        for book in search:
            keyboard.append(InlineKeyboardButton(text=book.name, callback_data=CheckBookCB(action='check_book', book=book.id).pack()))

        pagination.row(*keyboard)
        pagination.adjust(6)

        if keyboard:
            await message.answer(text='Результаты поиска!', reply_markup=pagination.as_markup())
            return
        await message.answer(text='Похоже ничего не нашлось... попробуй еще раз!')

    @on.callback_query(CheckBookCB.filter(F.action == "check_book"))
    async def check_book(self, callback: CallbackQuery, callback_data: CheckBookCB, state: FSMContext) -> None:
        await state.update_data(book=callback_data.book)
        book = base.Book.get(callback_data.book)

        await callback.message.answer(text=f'Название книги: {book.name}\n'
                                           f'Описание книги: {book.description}\n'
                                           f'Автор книги: {book.author}\n'
                                           f'Жанр книги: {book.genre}',
                                      reply_markup=Keyboards.DELETE_KEYBOARD)

    @on.callback_query(F.data == 'delete_book')
    async def delete_book(self, callback: CallbackQuery, state: FSMContext) -> None:
        user_data = await state.get_data()
        book_id = user_data.get('book')

        book = base.Book.get_or_none(id=book_id)

        if book is not None:
            book.delete_instance()

            await callback.answer(f'Книга с ID {book_id} был удален!')
            await self.wizard.exit()
            return

        await callback.answer('Данной книги нет в базе!')