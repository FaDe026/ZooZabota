from pydantic import BaseModel
from datetime import datetime

from src.enums import GenderEnum


class DogAddSchema(BaseModel):
    name: str
    age: int

class DogGetSchema(BaseModel):
    id: int
    name: str
    age: int
    breed: str
    description: str
    intake_date: datetime
    veterinary_passport: bool
    gender: GenderEnum