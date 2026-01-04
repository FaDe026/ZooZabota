from fastapi import APIRouter
from sqlalchemy import text
from src.database import engine, Base

router = APIRouter(prefix="/setup_database", tags=["Database"])
@router.post("/")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        # await conn.run_sync(Base.metadata.create_all)
