from sqlalchemy import Column, Integer, String, Boolean

from api.database.db_session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, index=True, unique=True, nullable=False)
    is_authorized = Column(Boolean, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
