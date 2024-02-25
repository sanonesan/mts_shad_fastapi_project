from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

# from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.configurations.auth import utils as auth_utils

from src.models.books import Book
from src.models.sellers import Seller

from src.schemas import (
    IncomingSeller,
    UpdateSellerData,
    ReturnedSeller,
    ReturnedAllSellers,
    ReturnedSellerFull,
)


sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

# Больше не симулируем хранилище данных. Подключаемся к реальному, через сессию.
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: DBSession):
    """
    Handle to create new seller
    """
    new_seller = Seller(
        first_name=seller.first_name,
        second_name=seller.second_name,
        email=seller.email,
        password=seller.password,
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    """
    Handle to get list of all sellers
    """
    query = select(Seller)
    res = await session.execute(query)
    sellers = res.scalars().all()

    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=ReturnedSellerFull)
async def get_seller(seller_id: int, session: DBSession):
    """
    Handle to get information about seller with its books
    """
    if seller := await session.get(Seller, seller_id):

        # Get seller's books by seller_id
        book_cols_to_select = [
            Book.id,
            Book.title,
            Book.author,
            Book.year,
            Book.count_pages,
        ]
        books = await session.execute(
            select(Book)
            .filter_by(seller_id=seller_id)
            .options(
                load_only(*book_cols_to_select),
            )
        )

        res = {}
        res["id"] = seller.id
        res["first_name"] = seller.first_name
        res["second_name"] = seller.second_name
        res["email"] = seller.email
        res["books"] = books.scalars().all()

        return res

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@sellers_router.put("/{seller_id}", response_model=ReturnedSeller)
async def update_seller(seller_id: int, new_data: UpdateSellerData, session: DBSession):
    """
    Handle to update seller's data
    """
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.first_name = new_data.first_name
        updated_seller.second_name = new_data.second_name
        updated_seller.email = new_data.email

        await session.flush()

        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@sellers_router.delete("/{seller_id}")
async def delete_book(seller_id: int, session: DBSession):
    """
    Handle to delete seller by id from DB. His books will be deteted too.
    """
    if deleted_seller := await session.get(Seller, seller_id):
        # ic(deleted_seller)
        if deleted_seller:
            await session.delete(deleted_seller)

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )  # Response может вернуть текст и метаданные.
    return Response(status_code=status.HTTP_404_NOT_FOUND)
