from typing import Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery

from bot.keyboards.base import Keyboards
from bot.fabrics.fabrics import ButtonsCB, Action
from bot.database import base

router: Final[Router] = Router(name=__name__)


class Genre_book(Scene, state="genre_book"):
    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery):
        raw_genres = base.Book.select().order_by(base.Book.id.desc()).limit(3)
        genres: list = []

        for genre in raw_genres:
            genres.append(genre.genre)

        result_genres = ', '.join(genres)

        await callback.message.edit_text(
            text=f"Напишите жанр книги\n\nПоследние 3 жанра введеные пользователями: {result_genres}",
            reply_markup=Keyboards.BACK_KEYBOARD
        )

    @on.message(F.text)
    async def genre_writing(self, message: Message, state: FSMContext) -> None:
        await state.update_data(choosen_genre=message.text)

        await message.answer(
            f"Установленный вами жанр: {message.text}",
        )

    @on.callback_query(ButtonsCB.filter(F.action == Action.BACK), after=After.goto('add_book'))
    async def back(self, _: CallbackQuery) -> None:
        pass