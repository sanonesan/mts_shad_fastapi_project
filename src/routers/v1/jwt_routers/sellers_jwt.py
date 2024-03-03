from fastapi import APIRouter, Depends, Response, status, Form
from pydantic import EmailStr

# from icecream import ic
from sqlalchemy import select

from src.configurations.database import get_async_session
from src.configurations.auth import utils as auth_utils

# from src.models.books_jwt import BookJWT
from src.models.sellers_jwt import SellerJWT

from src.schemas import (
    TokenInfo,
    LogInSellerJWT,
    ReturnedSellerJWT,
    SignInSellerJWT,
    ReturnedAllSellersJWT,
    ReturnedSellerJWTFull,
)

from .utils.utils_jwt import (
    get_current_auth_seller,
    get_current_auth_seller_full,
    validate_auth_user,
    validate_registration_user,
)

seller_jwt_router = APIRouter(tags=["JWT"], prefix="/jwt")


@seller_jwt_router.post(
    "/signup", response_model=ReturnedSellerJWT, status_code=status.HTTP_201_CREATED
)
async def register_seller_jwt(
    seller: SignInSellerJWT = Depends(validate_registration_user),
    session=Depends(get_async_session),
):
    """
    Handle to create (register) new seller
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


@seller_jwt_router.post("/login", response_model=TokenInfo)
async def auth_seller_jwt(
    seller: LogInSellerJWT = Depends(validate_auth_user),
):
    """
    Handle to login seller
    (return his token: check if email and password are in DB and are correct)
    """
    jwt_payload = {
        "email": seller.email,
        "seller_id": seller.id,
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@seller_jwt_router.get("/sellers/me/info", response_model=ReturnedSellerJWTFull)
async def auth_seller_jwt_check_self_info(
    seller: ReturnedSellerJWTFull = Depends(get_current_auth_seller_full),
):
    """
    Handle to get seller's info by his jwt
    """
    return seller


@seller_jwt_router.put("/sellers/me/info/update", response_model=ReturnedSellerJWT)
async def update_seller_jwt(
    email: None | EmailStr = Form(default=None),
    first_name: None | str = Form(default=None),
    second_name: None | str = Form(default=None),
    seller: ReturnedSellerJWT = Depends(get_current_auth_seller),
    session=Depends(get_async_session),
):
    """
    Handle to update current authorized seller's data
    """
    if email != None:
        seller.email = email

    if first_name != None:
        seller.first_name = first_name

    if second_name != None:
        seller.second_name = second_name

    await session.flush()

    return seller


@seller_jwt_router.delete("/sellers/me/delete_account")
async def delete_seller_jwt(
    seller: ReturnedSellerJWT = Depends(get_current_auth_seller),
    session=Depends(get_async_session),
):
    """
    Handle to delete current authorized seller from DB. Seller's books will be deteted too.
    """
    await session.delete(seller)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@seller_jwt_router.get("/sellers/list", response_model=ReturnedAllSellersJWT)
async def get_all_sellers_jwt(
    session=Depends(get_async_session),
):
    """
    Handle to get list of all sellers
    """
    res = await session.execute(select(SellerJWT))
    sellers = res.scalars().all()

    return {"sellers": sellers}
