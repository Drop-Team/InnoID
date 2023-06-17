import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import App


class IAppRepository(ABC):
    @abstractmethod
    def get_by_id(self, app_id: uuid.UUID) -> Optional[App]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, offset: int, limit: int) -> list[App]:
        raise NotImplementedError

    @abstractmethod
    def add(self, app: App) -> App:
        raise NotImplementedError

    @abstractmethod
    def remove(self, app_id: uuid.UUID) -> Optional[App]:
        raise NotImplementedError

    @abstractmethod
    def next_id(self) -> uuid.UUID:
        raise NotImplementedError
