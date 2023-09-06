import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelegramConnection:
    user_id: uuid.UUID
    created: datetime
    telegram_id: str
