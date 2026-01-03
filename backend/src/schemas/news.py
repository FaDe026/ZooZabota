from pydantic import BaseModel, field_serializer, ConfigDict
from datetime import datetime
from typing import List
from .tags import TagResponseSchema


class NewsAddSchema(BaseModel):
    title: str
    body: str
    tags: str | None = None
    preview: str | None = None


class NewsGetSchema(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    author_id: int
    tags: List[TagResponseSchema]
    preview: str | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('date')
    def serialize_date(self, dt: datetime) -> str:
        return dt.strftime('%Y-%m-%d %H:%M')