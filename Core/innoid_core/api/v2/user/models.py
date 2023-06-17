import uuid

from pydantic import BaseModel


class User(BaseModel):
    user_id: uuid.UUID
    email: str


class UserCreate(BaseModel):
    email: str
