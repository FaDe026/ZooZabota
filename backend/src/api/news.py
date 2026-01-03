from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models.news import NewsModel
from src.models.tags import TagModel
from src.schemas.news import NewsGetSchema
from datetime import datetime
from src.models.user import UserModel
from src.utils.auth import get_current_user
from src.utils.validate_image import validate_and_save_news_image
from pathlib import Path
from typing import Union


router = APIRouter(prefix="/news", tags=["News"])


def parse_tag_ids(tag_ids_str: str | None) -> list[int]:
    """Преобразует строку '1,2,3' в список [1, 2, 3]."""
    if not tag_ids_str:
        return []
    try:
        return [int(x.strip()) for x in tag_ids_str.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат tag_ids. Ожидаются целые числа, разделённые запятыми (например: 1,2,3)."
        )


@router.post("/", response_model=NewsGetSchema)
async def add_news(
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
    title: str = Form(...),
    body: str = Form(...),
    tag_ids: str | None = Form(
        None,
        description="Список ID тегов через запятую (например: 1,2,3)"
    ),
    preview: str | None = Form(None),
    file: UploadFile = File(None),
):
    """Создать новую новость с привязкой тегов по ID."""
    image_url = await validate_and_save_news_image(file)

    news_tags = []
    if tag_ids:
        ids = parse_tag_ids(tag_ids)
        if ids:
            result = await session.execute(select(TagModel).where(TagModel.id.in_(ids)))
            found_tags = result.scalars().all()
            found_ids = {t.id for t in found_tags}
            missing = set(ids) - found_ids
            if missing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Теги с ID {sorted(missing)} не найдены."
                )
            news_tags = found_tags

    new_news = NewsModel(
        title=title,
        date=datetime.now().replace(microsecond=0),
        body=body,
        author_id=current_user.id,
        preview=preview,
        image_url=image_url,
        tags=news_tags,
    )
    session.add(new_news)
    await session.commit()
    await session.refresh(new_news, attribute_names=["tags", "author"])
    return new_news


@router.get("/", response_model=list[NewsGetSchema])
async def get_all_news(session: AsyncSession = Depends(get_session)):
    """Получить все новости с тегами."""
    result = await session.execute(
        select(NewsModel).options(
        )
    )
    return result.scalars().all()


@router.get("/{news_id}", response_model=NewsGetSchema)
async def get_news_by_id(news_id: int, session: AsyncSession = Depends(get_session)):
    """Получить новость по ID с тегами."""
    result = await session.execute(select(NewsModel).where(NewsModel.id == news_id))
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
    tag_ids: str | None = Form(
        None,
        description="Список ID тегов через запятую (например: 1,2,3)"
    ),
    preview: str | None = Form(None),
    file: UploadFile = File(None),
):
    """Полное обновление новости с заменой тегов."""
    result = await session.execute(select(NewsModel).where(NewsModel.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат даты. Используйте: YYYY-MM-DD HH:MM"
        )

    image_url = await validate_and_save_news_image(file)

    news.title = title
    news.body = body
    news.date = parsed_date
    news.preview = preview
    news.image_url = image_url

    news.tags = []
    if tag_ids:
        ids = parse_tag_ids(tag_ids)
        if ids:
            result = await session.execute(select(TagModel).where(TagModel.id.in_(ids)))
            found_tags = result.scalars().all()
            found_ids = {t.id for t in found_tags}
            missing = set(ids) - found_ids
            if missing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Теги с ID {sorted(missing)} не найдены."
                )
            news.tags = found_tags

    await session.commit()
    await session.refresh(news, attribute_names=["tags", "author"])
    return news


@router.patch("/{news_id}", response_model=NewsGetSchema)
async def partial_update_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
    title: str | None = Form(None),
    body: str | None = Form(None),
    date_str: str | None = Form(None),
    tag_ids: str | None = Form(
        None,
        description="Список ID тегов через запятую (например: 1,2,3). Передайте пустую строку, чтобы удалить все теги."
    ),
    preview: str | None = Form(None),
    file: Union[UploadFile, str] = File(None),
):
    """Частичное обновление новости. Теги можно обновить или удалить."""
    result = await session.execute(select(NewsModel).where(NewsModel.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    update_data = {}

    if title is not None:
        update_data["title"] = title
    if body is not None:
        update_data["body"] = body
    if preview is not None:
        update_data["preview"] = preview

    if date_str is not None and date_str.strip():
        try:
            parsed_date = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M")
            update_data["date"] = parsed_date
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Неверный формат даты. Используйте: YYYY-MM-DD HH:MM"
            )

    if isinstance(file, UploadFile):
        image_url = await validate_and_save_news_image(file)
        update_data["image_url"] = image_url

    for key, value in update_data.items():
        setattr(news, key, value)

    if tag_ids is not None:
        ids = parse_tag_ids(tag_ids)
        if ids:
            result = await session.execute(select(TagModel).where(TagModel.id.in_(ids)))
            found_tags = result.scalars().all()
            found_ids = {t.id for t in found_tags}
            missing = set(ids) - found_ids
            if missing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Теги с ID {sorted(missing)} не найдены."
                )
            news.tags = found_tags
        else:
            news.tags = []

    await session.commit()
    await session.refresh(news, attribute_names=["tags", "author"])
    return news


@router.delete("/{news_id}")
async def delete_news(news_id: int, session: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    """Удалить новость и связанные данные."""
    result = await session.execute(select(NewsModel).where(NewsModel.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    if news.image_url:
        file_path = Path(news.image_url.lstrip("/"))
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    await session.delete(news)
    await session.commit()
    return {"message": "Новость удалена"}