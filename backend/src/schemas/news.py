from pydantic import BaseModel
from datetime import datetime


class NewsAddSchema(BaseModel):
    title: str
    date: datetime
    body: str
    author_id: int
    tags: str | None = None
    preview: str | None = None
    news_image_id: int | None = None


class NewsGetSchema(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    author_id: int
    tags: str | None = None
    preview: str | None = None
    news_image_id: int | None = None

    class Config:
        from_attributes = True