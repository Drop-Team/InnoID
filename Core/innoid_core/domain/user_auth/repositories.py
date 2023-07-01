import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import UserRefreshToken


class IUserRefreshTokenRepository(ABC):
    @abstractmethod
    def get_by_id(self, token_id: uuid.UUID) -> Optional[UserRefreshToken]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_jwt_refresh_token: UserRefreshToken) -> UserRefreshToken:
        raise NotImplementedError

    @abstractmethod
    def remove(self, token_id: uuid.UUID) -> Optional[UserRefreshToken]:
        raise NotImplementedError

    @abstractmethod
    def next_id(self) -> uuid.UUID:
        raise NotImplementedError
