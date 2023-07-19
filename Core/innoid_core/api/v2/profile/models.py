import uuid
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: uuid.UUID
    email: str


class UserCreate(BaseModel):
    email: str


class UserAppCreate(BaseModel):
    name: str


class UserApp(BaseModel):
    id: uuid.UUID
    name: str


class UserTelegramConnection(BaseModel):
    created: datetime
    telegram_id: str

class UserIdCode(BaseModel):
    code: int
