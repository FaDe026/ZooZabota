from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.tags_dogs import tag_dog
from typing import List

class TagModel(Base):
    __tablename__ = 'tag'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]

    dogs: Mapped[List["DogModel"]] = relationship(
        "DogModel",
        secondary=tag_dog,
        back_populates="tags",
        passive_deletes=True
    )