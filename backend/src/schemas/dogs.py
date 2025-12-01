from pydantic import BaseModel

class DogAddSchema(BaseModel):
    name: str
    age: int

class DogGetSchema(BaseModel):
    id : int
    name: str
    age: int