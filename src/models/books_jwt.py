from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .sellers_jwt import SellerJWT


class BookJWT(BaseModel):
    __tablename__ = "books_jwt_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(SellerJWT.id, ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int]
    count_pages: Mapped[int]
