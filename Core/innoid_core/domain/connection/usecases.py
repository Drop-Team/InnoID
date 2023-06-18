import uuid
from datetime import datetime

from .entities import TelegramConnection
from .errors import ConnectionNotFoundError
from .repositories import ITelegramConnectionRepository


class TelegramConnectionUseCase:
    tg_connection_repository: ITelegramConnectionRepository

    def __init__(self, telegram_connection_repository: ITelegramConnectionRepository):
        self.tg_connection_repository = telegram_connection_repository

    def get_by_user_id(self, user_id: uuid.UUID) -> TelegramConnection:
        connection = self.tg_connection_repository.get_by_user_id(user_id)
        if not connection:
            raise ConnectionNotFoundError()
        return connection

    def get_by_telegram_id(self, telegram_id: str) -> TelegramConnection:
        connection = self.tg_connection_repository.get_by_telegram_id(telegram_id)
        if not connection:
            raise ConnectionNotFoundError()
        return connection

    def create(self, user_id: uuid.UUID, telegram_id: str) -> TelegramConnection:
        connection = TelegramConnection(
            user_id=user_id,
            telegram_id=telegram_id,
            created=datetime.now(),
        )
        connection = self.tg_connection_repository.add(connection)
        return connection

    def delete(self, user_id: uuid.UUID) -> TelegramConnection:
        connection = self.tg_connection_repository.remove(user_id)
        if not connection:
            raise ConnectionNotFoundError()
        return connection
