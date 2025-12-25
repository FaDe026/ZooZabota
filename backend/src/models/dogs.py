from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.enums import GenderEnum
from sqlalchemy import String
from datetime import date
from sqlalchemy import Text


class DogModel(Base):
    __tablename__ = 'dog'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    age : Mapped[int]
    breed: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    intake_date: Mapped[date] = mapped_column(default=date.today, nullable=True)
    veterinary_passport: Mapped[bool]
    gender: Mapped[GenderEnum]
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)