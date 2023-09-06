import uuid
from typing import Union

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.postgresql.database import Base


class UserModel(Base):
    __tablename__ = "users"
    user_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    email: Union[str, Column] = Column(String, nullable=False, unique=True)
