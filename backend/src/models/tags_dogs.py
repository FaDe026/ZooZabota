from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base

tag_dog = Table(
    'tag_dog',
    Base.metadata,
    Column('dog_id', Integer, ForeignKey('dog.id', ondelete="CASCADE"), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"), primary_key=True),
)