import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class JWTRefreshToken:
    token_id: uuid.UUID
    user_id: uuid.UUID
    hashed_value: str
    expires: datetime

    @staticmethod
    def next_id() -> uuid.UUID:
        return uuid.uuid4()
