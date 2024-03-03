from typing import Annotated

from fastapi import APIRouter, Depends, Response, status, Form, HTTPException

# from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from src.configurations.database import get_async_session
from src.models.books_jwt import BookJWT

# from src.models.sellers import Seller

from src.schemas import (
    ReturnedAllBooks,
    ReturnedBook,
    ReturnedSellerJWT,
)

books_jwt_router = APIRouter(tags=["JWT"], prefix="/jwt")

from .utils.utils_jwt import (
    get_current_auth_seller,
)

# Больше не симулируем хранилище данных. Подключаемся к реальному, через сессию.
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@books_jwt_router.get("/books/list", response_model=ReturnedAllBooks)
async def get_all_books(session: DBSession):
    """
    Handle to get all books from DB
    """
    query = select(BookJWT)
    res = await session.execute(query)
    books = res.scalars().all()
    return {"books": books}


@books_jwt_router.get("/books/{book_id}", response_model=ReturnedBook)
async def get_book_by_id(book_id: int, session: DBSession):
    """
    Handle to get book from DB by its id
    """
    res = await session.get(BookJWT, book_id)
    return res


@books_jwt_router.post(
    "/sellers/me/books/add",
    response_model=ReturnedBook,
    status_code=status.HTTP_201_CREATED,
)
async def add_book_seller_jwt(
    title: str = Form(),
    author: str = Form(),
    year: int = Form(),
    count_pages: int = Form(),
    seller: ReturnedSellerJWT = Depends(get_current_auth_seller),
    session=Depends(get_async_session),
):
    """
    Handle to add new book for current authenticated seller
    """
    new_book = BookJWT(
        seller_id=seller.id,
        title=title,
        author=author,
        year=year,
        count_pages=count_pages,
    )
    session.add(new_book)
    await session.flush()

    return new_book


@books_jwt_router.put("/sellers/me/books/{book_id}/update", response_model=ReturnedBook)
async def update_book_seller_jwt(
    book_id: int,
    title: None | str = Form(default=None),
    author: None | str = Form(default=None),
    year: None | int = Form(default=None),
    count_pages: None | int = Form(default=None),
    seller: ReturnedSellerJWT = Depends(get_current_auth_seller),
    session=Depends(get_async_session),
):
    """
    Handle to update existing book for current authenticated seller.

    Only entered fields will be updated
    """
    if updated_book := await session.get(BookJWT, book_id):

        if updated_book.seller_id == seller.id:

            updated_book.seller_id = seller.id

            if author != None:
                updated_book.author = author
            if title != None:
                updated_book.title = title
            if year != None:
                updated_book.year = year
            if count_pages != None:
                updated_book.count_pages = count_pages

            await session.flush()

            return updated_book

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Book does not belong to current user",
        )

    return Response(status_code=HTTP_404_NOT_FOUND)


@books_jwt_router.delete("/sellers/me/books/{book_id}/delete_book")
async def delete_book_seller_jwt(
    book_id: int,
    seller: ReturnedSellerJWT = Depends(get_current_auth_seller),
    session=Depends(get_async_session),
):
    """
    Handle to add new book for current authenticated seller.
    """
    if deleted_book := await session.get(BookJWT, book_id):

        if deleted_book.seller_id == seller.id:
            await session.delete(deleted_book)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Book does not belong to current user",
        )

    return Response(status_code=HTTP_404_NOT_FOUND)
