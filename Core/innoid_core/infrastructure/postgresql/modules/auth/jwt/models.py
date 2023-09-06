import uuid
from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.postgresql.database import Base


class JWTRefreshTokenModel(Base):
    __tablename__ = "jwt_refresh_tokens"
    token_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True), primary_key=True)
    user_id: Union[uuid.UUID, Column] = Column(UUID(as_uuid=True))
    expires: Union[datetime, Column] = Column(DateTime(timezone=False), nullable=False)
    hashed_value: Union[str, Column] = Column(String, nullable=False)
