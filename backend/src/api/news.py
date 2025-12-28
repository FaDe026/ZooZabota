from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.news import NewsModel
from src.schemas.news import NewsAddSchema, NewsGetSchema
from datetime import datetime
from src.models.user import UserModel
from src.utils.auth import get_current_user

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/", response_model=NewsGetSchema)
async def add_news(news_data: NewsAddSchema, 
                   current_user: UserModel = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)):
    new_news = NewsModel(
        title=news_data.title,
        date=news_data.date or datetime.now().replace(microsecond=0, second=0),
        body=news_data.body,
        author_id=current_user.id,
        tags=news_data.tags,
        preview=news_data.preview,
        news_image_id=news_data.news_image_id
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
async def update_news(news_id: int, news_data: NewsAddSchema, session: AsyncSession = Depends(get_session)):
    """Обновить новость по ID"""
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    news.title = news_data.title
    news.date = news_data.date
    news.body = news_data.body
    news.author_id = news_data.author_id
    news.tags = news_data.tags
    news.preview = news_data.preview
    news.news_image_id = news_data.news_image_id

    await session.commit()
    await session.refresh(news)
    return news


@router.delete("/{news_id}")
async def delete_news(news_id: int, session: AsyncSession = Depends(get_session)):
    """Удалить новость по ID"""
    query = select(NewsModel).where(NewsModel.id == news_id)
    result = await session.execute(query)
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    await session.delete(news)
    await session.commit()
    return {"message": "Новость удалена"}