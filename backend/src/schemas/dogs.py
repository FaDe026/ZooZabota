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

    class Config:
        from_attributes = True
