import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApiKey:
    app_id: uuid.UUID
    created: datetime
    hashed_value: str
