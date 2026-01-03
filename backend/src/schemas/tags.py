from pydantic import BaseModel, ConfigDict


class TagAddSchema(BaseModel):
    name: str

class TagResponseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
