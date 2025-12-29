from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.news import NewsModel
from src.schemas.news import NewsGetSchema
from datetime import datetime
from src.models.user import UserModel
from src.utils.auth import get_current_user
from src.utils.validate_image import validate_and_save_news_image
from pathlib import Path
from typing import Union, Annotated

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/", response_model=NewsGetSchema)
async def add_news(
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
    title: str = Form(...),
    body: str = Form(...),
    tags: str | None = Form(None),
    preview: str | None = Form(None),
    file: UploadFile = File(None),
):
    """
    Создать новую новость.
    Автор устанавливается автоматически на основе текущего пользователя.
    Дата публикации устанавливается автоматически.
    """
    image_url = await validate_and_save_news_image(file)

    new_news = NewsModel(
        title=title,
        date=datetime.now().replace(microsecond=0),
        body=body,
        author_id=current_user.id,
        tags=tags,
        preview=preview,
        image_url=image_url,
    )
    session.add(new_news)
    await session.commit()
    await session.refresh(new_news)
    return new_news


@router.get("/", response_model=list[NewsGetSchema])
async def get_all_news(session: AsyncSession = Depends(get_session)):
    """Получить все новости"""
    query = select(NewsModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{news_id}", response_model=NewsGetSchema)
async def get_news_by_id(news_id: int, session: AsyncSession = Depends(get_session)):
    """Получить новость по ID"""
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news


@router.put("/{news_id}", response_model=NewsGetSchema)
async def update_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
    title: str = Form(...),
    body: str = Form(...),
    date_str: str = Form(..., description="Дата в формате YYYY-MM-DD HH:MM"),
    tags: str | None = Form(None),
    preview: str | None = Form(None),
    file: UploadFile = File(None),
):
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(400, detail="Неверный формат даты. Используйте: YYYY-MM-DD HH:MM")

    image_url = await validate_and_save_news_image(file)

    news.title = title
    news.body = body
    news.date = parsed_date
    news.tags = tags
    news.preview = preview
    news.image_url = image_url

    await session.commit()
    await session.refresh(news)
    return news


@router.patch("/{news_id}", response_model=NewsGetSchema)
async def partial_update_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
    title: str | None = Form(None),
    body: str | None = Form(None),
    date_str: str | None = Form(None),
    tags: str | None = Form(None),
    preview: str | None = Form(None),
    file: Union[UploadFile, str] = File(None),
):
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    update_data = {}

    if title is not None:
        update_data["title"] = title
    if body is not None:
        update_data["body"] = body
    if tags is not None:
        update_data["tags"] = tags
    if preview is not None:
        update_data["preview"] = preview

    if date_str is not None:
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            update_data["date"] = parsed_date
        except ValueError:
            raise HTTPException(400, detail="Неверный формат даты. Используйте: YYYY-MM-DD HH:MM")

    if isinstance(file, UploadFile):
        image_url = await validate_and_save_news_image(file)
        update_data["image_url"] = image_url

    for key, value in update_data.items():
        setattr(news, key, value)

    await session.commit()
    await session.refresh(news)
    return news


@router.delete("/{news_id}")
async def delete_news(news_id: int, session: AsyncSession = Depends(get_session)):
    """
    Удалить новость по ID.
    Также удаляет связанный файл изображения с диска, если он существует.
    """
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    if news.image_url:
        relative_path = news.image_url.lstrip("/")
        file_path = Path(relative_path)
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    await session.delete(news)
    await session.commit()
    return {"message": "Новость удалена"}