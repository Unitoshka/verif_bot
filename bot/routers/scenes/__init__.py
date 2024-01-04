from typing import Final

from aiogram import Router, F

from . import add_book, title_book, author_book, genre_book, description_book, all_books, search

router: Final[Router] = Router(name=__name__)
router.include_routers(add_book.router, title_book.router, description_book.router, author_book.router, genre_book.router)

router.callback_query.register(add_book.Add_book.as_handler(), F.data == "add_book")
router.callback_query.register(title_book.Title_book.as_handler(), F.data == "title_book")
router.callback_query.register(description_book.Description_book.as_handler(), F.data == "description_book")
router.callback_query.register(author_book.Author_book.as_handler(), F.data == "author_book")
router.callback_query.register(genre_book.Genre_book.as_handler(), F.data == "genre_book")

router.callback_query.register(all_books.All_books.as_handler(), F.data == "all_books")
router.callback_query.register(search.Search.as_handler(), F.data == "search")
