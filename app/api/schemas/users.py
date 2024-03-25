from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str


class UserBase(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
