from __future__ import annotations
from datetime import date
from typing import List
from pydantic import BaseModel
from src.enums import GenderEnum
from src.schemas.tags import TagResponseSchema

class DogAddSchema(BaseModel):
    name: str
    age: int
    breed: str
    description: str
    intake_date: date | None = None
    veterinary_passport: bool
    gender: GenderEnum

class DogResponseSchema(BaseModel):
    id: int
    name: str
    age: int
    breed: str
    description: str
    intake_date: date
    veterinary_passport: bool
    gender: GenderEnum
    image_url: str | None = None
    tags: List[TagResponseSchema]

    class Config:
        from_attributes = True

class DogImagesRandomSchema(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True
