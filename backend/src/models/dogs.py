from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class DogModel(Base):
    __tablename__ = 'dog'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    age : Mapped[int]