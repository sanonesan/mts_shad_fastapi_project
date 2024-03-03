from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core import PydanticCustomError


from .books import ReturnedBookForSeller

__all__ = [
    "IncomingSeller",
    "ReturnedAllSellers",
    "ReturnedSeller",
    "ReturnedSellerFull",
    "UpdateSellerData",
]


class BaseSeller(BaseModel):
    """
    Class with basic seller fields
    """

    first_name: str
    second_name: str | None = None
    email: EmailStr
    password: str


class IncomingSeller(BaseSeller):
    """
    Class for validation of entered seller data
    """

    second_name: str | None = None

    @field_validator("password")  # password validator
    @staticmethod
    def validate_password(val: str):
        if len(val) <= 4:
            raise PydanticCustomError("Validation error", "password is too short!")
        return val


class UpdateSellerData(BaseModel):
    """
    Class for return info about seller by its id
    to update info
    do not change id in db
    """

    first_name: str
    second_name: str
    email: EmailStr


class ReturnedSeller(BaseModel):
    """
    Class for return info about seller by its id
    """

    id: int
    first_name: str
    second_name: str
    email: EmailStr


class ReturnedAllSellers(BaseModel):
    """
    Class for return array of object Seller
    """

    sellers: list[ReturnedSeller]


class ReturnedSellerFull(ReturnedSeller):
    """
    Class to return seller with his books
    """

    books: list[ReturnedBookForSeller]
