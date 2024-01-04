from typing import Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery

from bot.keyboards.base import Keyboards
from bot.fabrics.fabrics import ButtonsCB, Action

router: Final[Router] = Router(name=__name__)


class Author_book(Scene, state="author_book"):
    @on.callback_query.enter()
    async def on_enter(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Напишите автора книги",
            reply_markup=Keyboards.BACK_KEYBOARD
        )

    @on.message(F.text)
    async def author_writing(self, message: Message, state: FSMContext) -> None:
        await state.update_data(choosen_author=message.text)

        await message.answer(
            f"Установленный вами автор: {message.text}",
        )

    @on.callback_query(ButtonsCB.filter(F.action == Action.BACK), after=After.goto('add_book'))
    async def back(self, _: CallbackQuery) -> None:
        pass
