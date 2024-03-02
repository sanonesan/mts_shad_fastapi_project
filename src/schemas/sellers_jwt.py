from pydantic import BaseModel, EmailStr

from .books import ReturnedBookForSeller

__all__ = [
    "SignInSellerJWT",
    "LogInSellerJWT",
    "ReturnedAllSellersJWT",
    "ReturnedSellerJWT",
    "ReturnedSellerJWTFull",
    "UpdateSellerDataJWT",
]


class BaseSellerJWT(BaseModel):
    """
    Class with basic seller fields
    """

    email: EmailStr
    password: str


class SignInSellerJWT(BaseSellerJWT):
    """
    Class for seller registration data
    """

    first_name: str = "None"
    second_name: str = "None"

    pass


class LogInSellerJWT(BaseSellerJWT):
    """
    Class seller log in
    """

    id: int

    pass

    # second_name: str | None = None
    #
    # @field_validator("password")  # password validator
    # @staticmethod
    # def validate_password(val: str):
    #     if len(val) <= 4:
    #         raise PydanticCustomError("Validation error", "password is too short!")
    #     return val


class UpdateSellerDataJWT(BaseModel):
    """
    Class for return info about seller by its id
    to update info
    do not change id in db
    """

    first_name: str
    second_name: str
    email: EmailStr


class ReturnedSellerJWT(BaseModel):
    """
    Class for return info about seller by its id
    """

    id: int
    first_name: str
    second_name: str
    email: EmailStr


class ReturnedAllSellersJWT(BaseModel):
    """
    Class for return array of object Seller
    """

    sellers: list[ReturnedSellerJWT]


class ReturnedSellerJWTFull(ReturnedSellerJWT):
    """
    Class to return seller with his books
    """

    books: list[ReturnedBookForSeller]
