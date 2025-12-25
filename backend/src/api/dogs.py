from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.api.dependencies import SessionDep
from src.models.dogs import DogModel
from src.schemas.dogs import DogAddSchema, DogResponseSchema
from pathlib import Path as SysPath
from sqlalchemy import select
import uuid
from typing import Optional
from src.enums import GenderEnum
from datetime import date

router = APIRouter(prefix="/dogs", tags=["Dogs"])

UPLOAD_DIR = SysPath("static/dogs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
    image_url = None
    if file:
        if file.content_type not in ("image/jpeg", "image/png", "image/jpg"):
            raise HTTPException(400, "Разрешены только JPEG и PNG изображения")

        ext = file.filename.split(".")[-1].lower() if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        image_url = f"/static/dogs/{filename}"

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