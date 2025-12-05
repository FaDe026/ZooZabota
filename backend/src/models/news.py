from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from src.database import Base

class NewsModel(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    # Author_ID(FK) — внешний ключ на автора Пока что не внешний
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    tags: Mapped[str] = mapped_column(String(500), nullable=True)
    preview: Mapped[str] = mapped_column(String(500), nullable=True)

    # News_Images(FK) — внешний ключ на изображения Пока что не внешний
    news_image_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # Связи (relationships) Их пока что нет
    #author = relationship("AuthorModel", back_populates="news")  # Связь с автором
    #image = relationship("ImageModel", back_populates="news")     # Связь с изображением (если нужно)