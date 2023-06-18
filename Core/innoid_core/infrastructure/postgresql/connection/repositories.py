import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.connection.entities import TelegramConnection
from domain.connection.repositories import ITelegramConnectionRepository
from .data_mappers import TelegramConnectionDataMapper
from .models import TelegramConnectionModel


class TelegramConnectionRepository(ITelegramConnectionRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[TelegramConnection]:
        telegram_connection_model = self.session.query(TelegramConnectionModel).filter_by(user_id=user_id).one_or_none()
        if telegram_connection_model:
            return TelegramConnectionDataMapper.model_to_entity(telegram_connection_model)
        return None

    def get_by_telegram_id(self, telegram_id: str) -> Optional[TelegramConnection]:
        telegram_connection_model = self.session.query(TelegramConnectionModel).filter_by(telegram_id=telegram_id).one_or_none()
        if telegram_connection_model:
            return TelegramConnectionDataMapper.model_to_entity(telegram_connection_model)
        return None

    def add(self, telegram_connection: TelegramConnection) -> TelegramConnection:
        telegram_connection_model = TelegramConnectionDataMapper.entity_to_model(telegram_connection)
        self.session.add(telegram_connection_model)
        self.session.commit()
        return TelegramConnectionDataMapper.model_to_entity(telegram_connection_model)

    def remove(self, user_id: uuid.UUID) -> Optional[TelegramConnection]:
        telegram_connection_model = self.session.query(TelegramConnectionModel).filter_by(user_id=user_id).one_or_none()
        if not telegram_connection_model:
            return None
        self.session.delete(telegram_connection_model)
        self.session.commit()
        return TelegramConnectionDataMapper.model_to_entity(telegram_connection_model)
