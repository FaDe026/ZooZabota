from fastapi import APIRouter

from src.api.dogs import router as dogs_router

main_router = APIRouter()

main_router.include_router(dogs_router)