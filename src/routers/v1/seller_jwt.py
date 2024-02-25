from typing import Annotated

from fastapi import APIRouter, Depends, Response, status, Form, HTTPException
from pydantic import EmailStr


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession, async_engine_from_config
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.configurations.database import get_async_session
from src.configurations.auth import utils as auth_utils

from src.models.books import Book
from src.models.sellers import Seller
from src.models.books_jwt import BookJWT
from src.models.sellers_jwt import SellerJWT

from src.schemas import (
    TokenInfo,
    LogInSellerJWT,
    ReturnedSellerJWT,
    SignInSellerJWT,
    # LogInSellerJWT,
    # SignInSellerJWT,
    # UpdateSellerData,
    # ReturnedSeller,
    # ReturnedAllSellers,
    # ReturnedSellerFull,
)


token_router = APIRouter(tags=["JWT"], prefix="/jwt")

http_bearer = HTTPBearer()

# Больше не симулируем хранилище данных. Подключаемся к реальному, через сессию.
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


async def validate_auth_user(
    email: EmailStr = Form(),
    password: str = Form(),
    session: DBSession | None = None,
):
    unauthed_exc = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )

    # seller = await session.execute(select(Seller).filter_by(email=email))
    # if seller := await session.execute(select(SellerJWT).filter_by(email=email)):
    #     seller = seller.scalars().first()
    #     if not auth_utils.validate_password(
    #         password=password,
    #         hashed_password=seller.password,
    #     ):
    #         return seller
    # else:
    #     return Response(status_code=unauthed_exc.status_code, content=unauthed_exc.detail)
    #
    # seller = seller.scalars().first()
    # if not auth_utils.validate_password(
    #     password=password,
    #     hashed_password=seller.password,
    # ):
    #     return seller
    #
    # return Response(status_code=unauthed_exc.status_code, content=unauthed_exc.detail)
    pass


#


@token_router.post("/log_in/", response_model=TokenInfo)
async def auth_seller_jwt(
    seller: LogInSellerJWT,
    session: DBSession,
):
    jwt_payload = {
        "email": seller.email,
        # "password": seller.password,
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@token_router.post(
    "/sign_in/", response_model=ReturnedSellerJWT, status_code=status.HTTP_201_CREATED
)
async def register_seller_jwt(
    seller: SignInSellerJWT,
    session: DBSession,
):
    """
    Handle to create new seller
    """
    new_seller_jwt = SellerJWT(
        first_name=seller.first_name,
        second_name=seller.second_name,
        email=seller.email,
        password=auth_utils.hash_password(seller.password),
    )

    session.add(new_seller_jwt)
    await session.flush()

    return new_seller_jwt


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> LogInSellerJWT:
    token = credentials.credentials

    ic(token)
    payload = auth_utils.decode_jwt(
        token=token,
    )
    ic(payload)
    print(payload)
    return payload


async def get_current_auth_seller(
    payload: dict = Depends(get_current_token_payload),
    session=Depends(get_async_session),
):

    email: str | None = payload.get("email")

    ic(email)
    print(email)

    cols_to_return = [
        SellerJWT.email,
        SellerJWT.password,
    ]
    if seller := await session.execute(select(SellerJWT).where(SellerJWT.email == email)):
        seller = seller.scalars().first()
        return {
            "email": seller.email,
            "password": seller.password,
        }

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="token invalid")
    # else:
    #     return {
    #         "email": email,
    #         "password": "asdgasg",
    #     }


# async def get_current_auth_seller(
#     seller: LogInSellerJWT = Depends(get_current_auth_seller_by_token),
#     # session: DBSession,
# ) -> LogInSellerJWT:
#     # unauthed_exc = HTTPException(
#     #     status_code=HTTP_401_UNAUTHORIZED,
#     #     detail="Invalid email or password",
#     # )
#     return seller

# if returned_seller := await session.execute(
#     select(SellerJWT).filter_by(email=seller.email)
# ):
#     returned_seller = returned_seller.scalars().first()
#     # res = {}
#     # res["id"] = returned_seller.id
#     # res["first_name"] = returned_seller.first_name
#     # res["second_name"] = returned_seller.second_name
#     # res["email"] = returned_seller.email
#     return returned_seller
#
# return Response(status_code=unauthed_exc.status_code, content=unauthed_exc.detail)


@token_router.get("/seller/me/", response_model=ReturnedSellerJWT)
async def auth_seller_jwt_check_self_info(
    seller: LogInSellerJWT = Depends(get_current_auth_seller),
    # session=Depends(get_async_session),
):
    return seller


# @token_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
# async def create_seller(seller: IncomingSeller, session: DBSession):
#     """
#     Handle to create new seller
#     """
#     new_seller = Seller(
#         first_name=seller.first_name,
#         second_name=seller.second_name,
#         email=seller.email,
#         password=auth_utils.hash_password(seller.password),
#     )
#
#     session.add(new_seller)
#     await session.flush()
#
#     return new_seller
#
#
# @token_router.get("/", response_model=ReturnedAllSellers)
# async def get_all_sellers(session: DBSession):
#     """
#     Handle to get list of all sellers
#     """
#     query = select(Seller)
#     res = await session.execute(query)
#     sellers = res.scalars().all()
#
#     return {"sellers": sellers}
#
#
# @token_router.get("/{seller_id}", response_model=ReturnedSellerFull)
# async def get_seller(seller_id: int, session: DBSession):
#     """
#     Handle to get information about seller with its books
#     """
#     if seller := await session.get(Seller, seller_id):
#
#         # Get seller's books by seller_id
#         book_cols_to_select = [
#             Book.id,
#             Book.title,
#             Book.author,
#             Book.year,
#             Book.count_pages,
#         ]
#         books = await session.execute(
#             select(Book)
#             .filter_by(seller_id=seller_id)
#             .options(
#                 load_only(*book_cols_to_select),
#             )
#         )
#
#         res = {}
#         res["id"] = seller.id
#         res["first_name"] = seller.first_name
#         res["second_name"] = seller.second_name
#         res["email"] = seller.email
#         res["books"] = books.scalars().all()
#
#         return res
#
#     return Response(status_code=status.HTTP_404_NOT_FOUND)
#
#
# @token_router.put("/{seller_id}", response_model=ReturnedSeller)
# async def update_seller(seller_id: int, new_data: UpdateSellerData, session: DBSession):
#     """
#     Handle to update seller's data
#     """
#     if updated_seller := await session.get(Seller, seller_id):
#         updated_seller.first_name = new_data.first_name
#         updated_seller.second_name = new_data.second_name
#         updated_seller.email = new_data.email
#
#         await session.flush()
#
#         return updated_seller
#
#     return Response(status_code=status.HTTP_404_NOT_FOUND)
#
#
# @token_router.delete("/{seller_id}")
# async def delete_book(seller_id: int, session: DBSession):
#     """
#     Handle to delete seller by id from DB. His books will be deteted too.
#     """
#     if deleted_seller := await session.get(Seller, seller_id):
#         # ic(deleted_seller)
#         if deleted_seller:
#             await session.delete(deleted_seller)
#
#         return Response(
#             status_code=status.HTTP_204_NO_CONTENT
#         )  # Response может вернуть текст и метаданные.
#     return Response(status_code=status.HTTP_404_NOT_FOUND)
