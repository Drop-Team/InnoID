import uuid
from typing import Union

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.postgresql.database import Base


class AppModel(Base):
    __tablename__ = "apps"
    app_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    name: Union[str, Column] = Column(String(255), nullable=False)
    owner_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), nullable=False)
