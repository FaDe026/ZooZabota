from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from pydantic import BaseModel
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class Base(DeclarativeBase):
    pass


class DogModel(Base):
    __tablename__ = 'dog'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    age : Mapped[int]


class DogAddSchema(BaseModel):
    name: str
    age: int  

class DogGetSchema(BaseModel):
    id : int
    name: str
    age: int    

@app.post("/dogs")
async def add_dog(data: DogAddSchema, session: SessionDep):
    new_dog = DogModel(
        name = data.name,
        age = data.age
    )
    session.add(new_dog)
    await session.commit()
    return {"ok": True}



@app.get("/dogs")
async def get_dogs(session: SessionDep):
    query = select(DogModel)
    result = await session.execute(query)
    return result.scalars().all()