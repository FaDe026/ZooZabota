from pydantic import BaseModel


class UserAddSchema(BaseModel):
    username: str
    password: str
    email: str
    role: str = "Admin"


class UserGetSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True