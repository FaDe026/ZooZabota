from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.api.dependencies import SessionDep
from src.models.dogs import DogModel
from src.schemas.dogs import DogAddSchema, DogResponseSchema
from sqlalchemy import select
from typing import Optional
from src.enums import GenderEnum
from datetime import date
from src.utils.validate_image import validate_and_save_dog_image

router = APIRouter(prefix="/dogs", tags=["Dogs"])

@router.post("", response_model=DogResponseSchema)
async def add_dog_with_avatar(
        session: SessionDep,
        name: str = Form(...),
        age: int = Form(...),
        breed: str = Form(...),
        description: str = Form(...),
        intake_date: Optional[str] = Form(None),
        veterinary_passport: bool = Form(...),
        gender: GenderEnum = Form(...),
        file: UploadFile = File(None),
):
    image_url = await validate_and_save_dog_image(file)

    parsed_intake_date = None
    if intake_date:
        try:
            parsed_intake_date = date.fromisoformat(intake_date)
        except ValueError:
            raise HTTPException(400, "Неверный формат даты. Используйте YYYY-MM-DD")

    new_dog = DogModel(
        name=name,
        age=age,
        breed=breed,
        description=description,
        intake_date=parsed_intake_date,
        veterinary_passport=veterinary_passport,
        gender=gender,
        image_url=image_url
    )

    session.add(new_dog)
    await session.commit()
    await session.refresh(new_dog)
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
async def put_dog(
        dog_id: int,
        session: SessionDep,
        name: str = Form(...),
        age: int = Form(...),
        breed: str = Form(...),
        description: str = Form(...),
        intake_date: Optional[str] = Form(None),
        veterinary_passport: bool = Form(...),
        gender: GenderEnum = Form(...),
        file: UploadFile = File(None)):
    query = select(DogModel).where(dog_id == DogModel.id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()
    if dog is None:
        raise HTTPException(status_code=404, detail="Информация о собаке не найдена")

    image_url = await validate_and_save_dog_image(file)

    parsed_intake_date = None
    if intake_date:
        try:
            parsed_intake_date = date.fromisoformat(intake_date)
        except ValueError:
            raise HTTPException(400, "Неверный формат даты. Используйте YYYY-MM-DD")


    dog.name = name
    dog.age = age
    dog.breed = breed
    dog.description = description
    dog.intake_date = parsed_intake_date if parsed_intake_date is not None else date.today
    dog.veterinary_passport = veterinary_passport
    dog.gender = gender
    dog.image_url = image_url

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