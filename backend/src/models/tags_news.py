from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base

tag_news = Table(
    "tag_news",
    Base.metadata,
    Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)
