from fastapi import APIRouter

from src.api.dogs import router as dogs_router
from src.api.news import router as news_router

main_router = APIRouter()

main_router.include_router(dogs_router)
main_router.include_router(news_router)