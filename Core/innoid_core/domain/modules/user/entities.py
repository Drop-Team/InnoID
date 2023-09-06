import uuid
from dataclasses import dataclass


@dataclass
class User:
    user_id: uuid.UUID
    email: str

    @staticmethod
    def next_id() -> uuid.UUID:
        return uuid.uuid4()
