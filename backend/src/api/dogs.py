from fastapi import APIRouter, HTTPException
from src.api.dependencies import SessionDep
from src.models.dogs import DogModel
from src.schemas.dogs import DogAddSchema, DogResponseSchema
from sqlalchemy import select


router = APIRouter(prefix="/dogs", tags=["Dogs"])


@router.post("", response_model=DogResponseSchema)
async def add_dog(data: DogAddSchema, session: SessionDep):
    new_dog = DogModel(
        name=data.name,
        age=data.age,
        breed=data.breed,
        description=data.description,
        intake_date=data.intake_date,
        veterinary_passport=data.veterinary_passport,
        gender=data.gender
    )
    session.add(new_dog)
    await session.commit()
    return new_dog


@router.get("", response_model=list[DogResponseSchema])
async def get_dogs(session: SessionDep):
    query = select(DogModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{dog_id}", response_model=DogResponseSchema)
async def get_dog(dog_id: int, session: SessionDep):
    query = select(DogModel).where(dog_id == DogModel.id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()
    if dog is None:
        raise HTTPException(status_code=404, detail="Информация о собаке не найдена")
    return dog


@router.put("/{dog_id}", response_model=DogResponseSchema)
async def put_dog(dog_id: int, data: DogAddSchema, session: SessionDep):
    query = select(DogModel).where(dog_id == DogModel.id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()
    if dog is None:
        raise HTTPException(status_code=404, detail="Информация о собаке не найдена")
    dog.name = data.name
    dog.age = data.age
    dog.breed = data.breed
    dog.description = data.description
    dog.intake_date = data.intake_date
    dog.veterinary_passport = data.veterinary_passport
    dog.gender = data.gender

    session.add(dog)
    await session.commit()
    await session.refresh(dog)
    return dog


@router.patch("/{dog_id}", response_model=DogResponseSchema)
async def partial_update_dog(dog_id: int, data: DogAddSchema, session: SessionDep):
    query = select(DogModel).where(dog_id == DogModel.id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()

    if dog is None:
        raise HTTPException(status_code=404, detail="Информация о собаке не найдена")

    update_dict = data.dict(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(dog, key, value)

    session.add(dog)
    await session.commit()
    await session.refresh(dog)
    return dog


@router.delete("/{dog_id}", response_model=DogResponseSchema)
async def delete_dog(dog_id: int, session: SessionDep):
    query = select(DogModel).where(dog_id == DogModel.id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()

    if dog is None:
        raise HTTPException(status_code=404, detail="Информация о собаке не найдена")

    await session.delete(dog)
    await session.commit()
    return {"message": f"Информация о собаке с {dog_id} удалена успешна"}