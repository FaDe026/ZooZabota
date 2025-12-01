from fastapi import APIRouter
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.models.dogs import DogModel
from src.schemas.dogs import DogAddSchema
from sqlalchemy import select

router = APIRouter()

@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@router.post("/dogs")
async def add_dog(data: DogAddSchema, session: SessionDep):
    new_dog = DogModel(
        name = data.name,
        age = data.age
    )
    session.add(new_dog)
    await session.commit()
    return {"ok": True}



@router.get("/dogs")
async def get_dogs(session: SessionDep):
    query = select(DogModel)
    result = await session.execute(query)
    return result.scalars().all()