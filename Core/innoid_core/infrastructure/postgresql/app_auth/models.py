import uuid
from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class AppApiKeyModel(Base):
    __tablename__ = "app_api_keys"
    app_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    created: Union[datetime, Column] = Column(DateTime(timezone=False), nullable=False)
    hashed_value: Union[str, Column] = Column(String, nullable=False)
