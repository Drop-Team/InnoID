import uuid

from pydantic import BaseModel


class App(BaseModel):
    app_id: uuid.UUID
    name: str
    owner_id: uuid.UUID


class AppWithApiKey(BaseModel):
    app_id: uuid.UUID
    name: str
    owner_id: uuid.UUID
    api_key: str


class AppCreate(BaseModel):
    name: str
    owner_id: uuid.UUID
