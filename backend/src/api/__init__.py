from fastapi import APIRouter

from src.api.dogs import router as dogs_router
from src.api.setup_server import router as setup_router

main_router = APIRouter()

main_router.include_router(dogs_router)
main_router.include_router(setup_router)