import enum
import uuid
from dataclasses import dataclass


class Permission(enum.Enum):
    ADMIN = "ADMIN"


@dataclass
class UserPermission:
    user_id: uuid.UUID
    permission: Permission


@dataclass
class AppPermission:
    app_id: uuid.UUID
    permission: Permission
