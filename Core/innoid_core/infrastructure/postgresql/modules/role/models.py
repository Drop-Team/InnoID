import uuid
from typing import Union

from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID

from domain.modules.role.entities import Role
from infrastructure.postgresql.database import Base


class UserRoleModel(Base):
    __tablename__ = "user_roles"
    user_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    role: Union[Role, Column] = Column(Enum(Role), primary_key=True)


class AppRoleModel(Base):
    __tablename__ = "app_roles"
    app_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    role: Union[Role, Column] = Column(Enum(Role), primary_key=True)
