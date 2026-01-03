from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base

if TYPE_CHECKING:
    from src.models.news import NewsModel

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="Admin")

    news: Mapped[list["NewsModel"]] = relationship("NewsModel",
                                                   back_populates="author",
                                                   cascade="all, delete-orphan")
