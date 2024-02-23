from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


from .books import ReturnedBookForSeller

__all__ = [
    "IncomingSeller",
    "ReturnedAllSellers",
    "ReturnedSeller",
    "ReturnedSellerFull",
    "UpdateSellerData",
]


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    second_name: str
    email: str
    password: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    first_name: str = "None"  # Пример присваивания дефолтного значения
    second_name: str = "None"  # Пример присваивания дефолтного значения
    email: str = "None"
    password: str = "None"

    @field_validator("password")  # Валидатор, проверяет что дата не слишком древняя
    @staticmethod
    def validate_password(val: str):
        if len(val) <= 4:
            raise PydanticCustomError("Validation error", "password is too short!")
        return val

    # pass


# Class for return info about seller by its id
# to update info
# do not change id in db
class UpdateSellerData(BaseModel):
    first_name: str
    second_name: str
    email: str


# Class for return info about seller by its id
class ReturnedSeller(BaseModel):
    id: int
    first_name: str
    second_name: str
    email: str


# Класс для возврата массива объектов Seller
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


# Class to return seller with his books
class ReturnedSellerFull(ReturnedSeller):
    books: list[ReturnedBookForSeller]
