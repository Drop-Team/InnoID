import uuid
from datetime import datetime

from pydantic import BaseModel


class UserId(BaseModel):
    user_id: uuid.UUID


class UserIdCode(BaseModel):
    code: int


class UserTelegramConnection(BaseModel):
    created: datetime
    user_id: uuid.UUID
    telegram_id: str


class UserTelegramConnectionCreate(BaseModel):
    user_id: uuid.UUID
    telegram_id: str
