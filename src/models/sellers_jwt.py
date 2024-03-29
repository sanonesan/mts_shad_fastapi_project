from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SellerJWT(BaseModel):
    __tablename__ = "sellers_jwt_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    second_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[bytes]  # = mapped_column(LargeBinary, nullable=False)
