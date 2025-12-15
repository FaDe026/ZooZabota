from fastapi import APIRouter

from src.api.dogs import router as dogs_router
from src.api.news import router as news_router
from src.api.user import router as users_router
from src.api.auth import router as auth_router

main_router = APIRouter()

main_router.include_router(dogs_router)
main_router.include_router(news_router)
main_router.include_router(users_router)
main_router.include_router(auth_router)