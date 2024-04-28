from pydantic import BaseModel


class Token(BaseModel):
    """Token model schema"""
    access_token: str
    type: str = "Bearer"
