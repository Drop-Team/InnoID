import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import TelegramConnection


class ITelegramConnectionRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[TelegramConnection]:
        raise NotImplementedError

    @abstractmethod
    def get_by_telegram_id(self, telegram_id: str) -> Optional[TelegramConnection]:
        raise NotImplementedError

    @abstractmethod
    def add(self, connection: TelegramConnection) -> TelegramConnection:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user_id: uuid.UUID) -> Optional[TelegramConnection]:
        raise NotImplementedError
