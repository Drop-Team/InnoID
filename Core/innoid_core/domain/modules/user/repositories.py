import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, offset: int, limit: int) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def next_id(self) -> uuid.UUID:
        raise NotImplementedError
