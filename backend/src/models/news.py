from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from src.database import Base

class NewsModel(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    tags: Mapped[str] = mapped_column(String(500), nullable=True)
    preview: Mapped[str] = mapped_column(String(500), nullable=True)

    # News_Images(FK) — внешний ключ на изображения Пока что не внешний
    news_image_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # Связи (relationships)
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="news")
    #image = relationship("ImageModel", back_populates="news")     # Связь с изображением (если нужно)