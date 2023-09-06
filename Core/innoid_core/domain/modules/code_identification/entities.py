import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserCodeIdentification:
    identification_id: uuid.UUID
    user_id: uuid.UUID
    created: datetime
    code: int
