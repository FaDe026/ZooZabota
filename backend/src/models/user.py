from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from src.database import Base

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="Admin")

    # Связи (relationships)
    # В ERD User связан с News как Author_ID. Добавим связь.
    news: Mapped[list["NewsModel"]] = relationship("NewsModel", back_populates="author", cascade="all, delete-orphan")

    # Если потребуется связь с другими сущностями (например, Request), добавьте их здесь.
    # requests: Mapped[list["RequestModel"]] = relationship("RequestModel", back_populates="user")