from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.utils.init_db import create_admin_user

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_admin_user()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)

app.include_router(main_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

