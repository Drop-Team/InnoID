import uuid
from dataclasses import dataclass


@dataclass
class AuthMethodResult:
    user_id: uuid.UUID | None
    app_id: uuid.UUID | None
