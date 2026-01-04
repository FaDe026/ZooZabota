from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.user import UserModel
from src.schemas.user import UserAddSchema, UserGetSchema
from src.utils.hashing import get_password_hash
from src.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserGetSchema)
async def add_user(
    user_data: UserAddSchema,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    """Создать нового пользователя"""
    existing_username = await session.execute(
        select(UserModel).where(UserModel.username == user_data.username)
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    existing_email = await session.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        username=user_data.username,
        password=hashed_password,
        email=user_data.email,
        role=user_data.role
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UserGetSchema])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserGetSchema)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.put("/{user_id}", response_model=UserGetSchema)
async def update_user(
    user_id: int,
    user_data: UserAddSchema,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    """Обновить пользователя"""
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user_data.username != user.username:
        existing = await session.execute(
            select(UserModel).where(UserModel.username == user_data.username)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Имя пользователя занято")

    if user_data.email != user.email:
        existing = await session.execute(
            select(UserModel).where(UserModel.email == user_data.email)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email уже используется")

    user.username = user_data.username
    user.password = get_password_hash(user_data.password)
    user.email = user_data.email
    user.role = user_data.role

    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int,
                      session: AsyncSession = Depends(get_session),
                      current_user: UserModel = Depends(get_current_user)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    await session.delete(user)
    await session.commit()
    return {"message": "Пользователь удален"}
