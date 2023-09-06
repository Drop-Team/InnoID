import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import ApiKey


class IApiKeyRepository(ABC):
    @abstractmethod
    def get_by_app_id(self, app_id: uuid.UUID) -> Optional[ApiKey]:
        raise NotImplementedError

    @abstractmethod
    def add(self, app_api_key: ApiKey) -> ApiKey:
        raise NotImplementedError

    @abstractmethod
    def remove(self, app_id: uuid.UUID) -> Optional[ApiKey]:
        raise NotImplementedError
