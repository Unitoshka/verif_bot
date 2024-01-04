from typing import Final, Any

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery

from bot.keyboards.base import create_keyboard, Keyboards

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message) -> TelegramMethod[Any]:
    return message.answer(text="Приветствую тебя в библиотеке! Что почитаем? ❄",
                          reply_markup=create_keyboard(Keyboards.START_MENU)
                          )


async def start_command_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text="Приветствую тебя в библиотеке! Что почитаем? ❄",
                                     reply_markup=create_keyboard(Keyboards.START_MENU)
                                     )
