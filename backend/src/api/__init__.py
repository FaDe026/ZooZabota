from fastapi import APIRouter

from src.api.dogs import router as dogs_router
from src.api.news import router as news_router
from src.api.user import router as users_router
from src.api.auth import router as auth_router
from src.api.setup_server import router as setup_router
from src.api.tags import router as tags_router
from src.api.requests import router as requests_router

main_router = APIRouter()

main_router.include_router(dogs_router)
main_router.include_router(setup_router)
main_router.include_router(tags_router)
main_router.include_router(news_router)
main_router.include_router(users_router)
main_router.include_router(auth_router)
main_router.include_router(requests_router)
