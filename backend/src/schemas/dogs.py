from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from datetime import date
from src.enums import GenderEnum


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

    class Config:
        from_attributes = True
