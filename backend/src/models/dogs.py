from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.enums import GenderEnum
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import Text


class DogModel(Base):
    __tablename__ = 'dog'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    age : Mapped[int]
    breed: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    intake_date: Mapped[datetime]
    veterinary_passport: Mapped[bool]
    gender: Mapped[GenderEnum]