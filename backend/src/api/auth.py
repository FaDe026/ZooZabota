from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.user import UserModel
from src.utils.auth import create_access_token
from src.utils.hashing import verify_password
from src.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    query = select(UserModel).where(UserModel.username == form_data.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
