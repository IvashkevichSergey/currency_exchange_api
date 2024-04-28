from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """Schema for user creating"""
    username: str
    password: str


class UserBase(UserCreate):
    """Base user schema"""
    id: int

    model_config = ConfigDict(from_attributes=True)
