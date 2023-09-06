import enum
import uuid
from dataclasses import dataclass


class Role(enum.Enum):
    ADMIN = "ADMIN"
    TELEGRAM_CONNECTIONS_CREATOR = "TELEGRAM_CONNECTIONS_CREATOR"
    USER = "USER"
    APP = "APP"


@dataclass
class UserRole:
    user_id: uuid.UUID
    role: Role


@dataclass
class AppRole:
    app_id: uuid.UUID
    role: Role
