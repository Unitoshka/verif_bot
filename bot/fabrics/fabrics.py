from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(Enum):
    EXIT = 'exit'
    BACK = 'back'


class ButtonsCB(CallbackData, prefix='buttons'):
    action: Action


class PaginationCB(CallbackData, prefix='pagination'):
    action: str
    offset: int = None
    page: int = None


class CheckBookCB(CallbackData, prefix='check_book'):
    action: str
    book: int