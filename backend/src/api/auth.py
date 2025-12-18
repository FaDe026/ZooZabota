from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.user import UserModel
from src.schemas.auth import UserLoginSchema
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    credentials: UserLoginSchema,
    session: AsyncSession = Depends(get_session)
):
    query = select(UserModel).where(UserModel.username == credentials.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    if user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    return {
        "message": "Успешный вход",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }

async def get_current_user(
    user_id: Optional[int] = Header(None, alias="X-User-ID"),
    session: AsyncSession = Depends(get_session)
) -> UserModel:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется X-User-ID в заголовке"
        )
    user = await session.get(UserModel, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    return user