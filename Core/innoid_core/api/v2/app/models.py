import uuid

from pydantic import BaseModel


class App(BaseModel):
    app_id: uuid.UUID
    name: str
    owner_id: uuid.UUID


class AppCreate(BaseModel):
    name: str
    owner_id: uuid.UUID
