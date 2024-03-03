from fastapi import Depends, Form, status, HTTPException
from pydantic import EmailStr

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import load_only

# from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.configurations.database import get_async_session
from src.configurations.auth import utils as auth_utils

from src.models.books_jwt import BookJWT
from src.models.sellers_jwt import SellerJWT

from src.schemas import (
    LogInSellerJWT,
    SignInSellerJWT,
)

http_bearer = HTTPBearer()


async def validate_registration_user(
    email: EmailStr = Form(),
    password: str = Form(),
    first_name: str = Form(default="None"),
    second_name: str = Form(default="None"),
    session=Depends(get_async_session),
) -> SignInSellerJWT:
    """
    User validation for registration:
        Check if there is info about seller in DB
        Check if password is not None
    """

    if seller := await session.execute(select(SellerJWT).where(SellerJWT.email == email)):
        if seller.scalars().first() != None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Try to login, this email is already taken",
            )

    if password == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter password",
        )

    if first_name == "None":
        # If needed field can be nesseccery to fill
        #
        # raise HTTPException(
        #     status_code=HTTP_401_UNAUTHORIZED,
        #     detail="Enter first_name",
        # )
        pass

    if second_name == "None":
        # If needed field can be nesseccery to fill
        #
        # raise HTTPException(
        #     status_code=HTTP_401_UNAUTHORIZED,
        #     detail="Enter second_name",
        # )
        pass

    new_seller = SignInSellerJWT(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
    )

    return new_seller


async def validate_auth_user(
    email: EmailStr = Form(),
    password: str = Form(),
    session=Depends(get_async_session),
) -> LogInSellerJWT:
    """
    User validation for login:
        Check if there is info about seller in DB
        Check if password is correct
    """
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )

    if login_seller := await session.execute(select(SellerJWT).where(SellerJWT.email == email)):
        login_seller = login_seller.scalars().first()
        if auth_utils.validate_password(
            password=password,
            hashed_password=login_seller.password,
        ):
            return login_seller

    raise unauthed_exc


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> LogInSellerJWT:
    """
    Get payload from token
    """
    token = credentials.credentials

    payload = auth_utils.decode_jwt(
        token=token,
    )

    return payload


async def get_current_auth_seller(
    payload: dict = Depends(get_current_token_payload),
    session=Depends(get_async_session),
):
    """
    Get info about user from DB with using token payload
    (token payload = {"seller_id": **id**})
    """

    seller_id: int | None = payload.get("seller_id")

    if seller := await session.get(SellerJWT, seller_id):
        return seller

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")


async def get_current_auth_seller_full(
    payload: dict = Depends(get_current_token_payload),
    session=Depends(get_async_session),
):
    """
    Get full info (with seller's books) about user from DB with using token payload
    (token payload = {"seller_id": **id**})
    """

    seller_id: int | None = payload.get("seller_id")

    seller = await session.get(SellerJWT, seller_id)
    # Get seller's books by seller_id
    book_cols_to_select = [
        BookJWT.id,
        BookJWT.title,
        BookJWT.author,
        BookJWT.year,
        BookJWT.count_pages,
    ]
    books = await session.execute(
        select(BookJWT)
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
