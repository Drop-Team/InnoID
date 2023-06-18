import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import AppApiKey


class IAppApiKeyRepository(ABC):
    @abstractmethod
    def get_by_app_id(self, app_id: uuid.UUID) -> Optional[AppApiKey]:
        raise NotImplementedError

    @abstractmethod
    def get_by_hashed_value(self, hashed_value: str) -> Optional[AppApiKey]:
        raise NotImplementedError

    @abstractmethod
    def add(self, app_api_key: AppApiKey) -> AppApiKey:
        raise NotImplementedError

    @abstractmethod
    def remove(self, app_id: uuid.UUID) -> Optional[AppApiKey]:
        raise NotImplementedError
