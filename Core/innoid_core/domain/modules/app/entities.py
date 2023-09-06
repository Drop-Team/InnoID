import uuid
from dataclasses import dataclass


@dataclass
class App:
    app_id: uuid.UUID
    name: str
    owner_id: uuid.UUID

    @staticmethod
    def next_id() -> uuid.UUID:
        return uuid.uuid4()
