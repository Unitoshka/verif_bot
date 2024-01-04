from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.fabrics.fabrics import ButtonsCB, Action


class Keyboards:
    START_MENU: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text="📖 Добавить книгу", callback_data="add_book"),
        InlineKeyboardButton(text="🔎 Найти книгу", callback_data="search"),
        InlineKeyboardButton(text="📚 Все книги", callback_data="all_books")
    ]

    CREATE_BOOK_KEYBOARD: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text="🏷️ Название", callback_data="title_book"),
        InlineKeyboardButton(text="📝 Описание", callback_data="description_book"),
        InlineKeyboardButton(text="✒️ Автор", callback_data="author_book"),
        InlineKeyboardButton(text="🎭 Жанр", callback_data="genre_book"),
        InlineKeyboardButton(text="✅ Создать", callback_data="finally_create"),
        InlineKeyboardButton(text="↩️ Назад", callback_data=ButtonsCB(action=Action.BACK).pack())
    ]

    BACK_BUTTON: list[InlineKeyboardButton] = [InlineKeyboardButton(text="↩️ Назад", callback_data=ButtonsCB(action=Action.BACK).pack())]
    DELETE_BUTTON: list[InlineKeyboardButton] = [InlineKeyboardButton(text="❌ Удалить", callback_data='delete_book')]

    BACK_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[BACK_BUTTON])
    DELETE_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[DELETE_BUTTON])


def create_keyboard(buttons: list[InlineKeyboardButton], row_width: int = 2) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(*buttons, width=row_width)
    return builder.as_markup()
