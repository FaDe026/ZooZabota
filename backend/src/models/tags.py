from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.tags_dogs import tag_dog
from src.models.tags_news import tag_news
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.models.news import NewsModel

class TagModel(Base):
    __tablename__ = 'tag'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]

    news: Mapped[List["NewsModel"]] = relationship(
        "NewsModel",
        secondary=tag_news,
        back_populates="tags",
        lazy="selectin",
    )