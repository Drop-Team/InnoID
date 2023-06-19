import uuid
from typing import Union

from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID

from domain.permission.entities import Permission
from ..database import Base


class UserPermissionModel(Base):
    __tablename__ = "user_permissions"
    user_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    permission: Union[Permission, Column] = Column(Enum(Permission), primary_key=True)


class AppPermissionModel(Base):
    __tablename__ = "app_permissions"
    app_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    permission: Union[Permission, Column] = Column(Enum(Permission), primary_key=True)
