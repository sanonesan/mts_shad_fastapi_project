from fastapi import APIRouter

from .v1.non_jwt_routers.books import books_router
from .v1.non_jwt_routers.sellers import sellers_router
from .v1.jwt_routers.sellers_jwt import seller_jwt_router
from .v1.jwt_routers.books_jwt import books_jwt_router

v1_router = APIRouter(tags=["v1"], prefix="/api/v1")


v1_router.include_router(books_router)
v1_router.include_router(sellers_router)
v1_router.include_router(seller_jwt_router)
v1_router.include_router(books_jwt_router)
