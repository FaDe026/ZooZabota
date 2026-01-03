from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from src.models.tags_news import tag_news

if TYPE_CHECKING:
    from src.models.user import UserModel
    from src.models.tags import TagModel

class NewsModel(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    preview: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    author: Mapped["UserModel"] = relationship("UserModel", back_populates="news")
    tags: Mapped[List["TagModel"]] = relationship(
        "TagModel",
        secondary=tag_news,
        back_populates="news",
        lazy="selectin",
    )
