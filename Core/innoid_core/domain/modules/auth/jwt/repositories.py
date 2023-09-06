import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import JWTRefreshToken


class IJWTRefreshTokenRepository(ABC):
    @abstractmethod
    def get_by_id(self, token_id: uuid.UUID) -> Optional[JWTRefreshToken]:
        raise NotImplementedError

    @abstractmethod
    def add(self, jwt_refresh_token: JWTRefreshToken) -> JWTRefreshToken:
        raise NotImplementedError

    @abstractmethod
    def remove(self, token_id: uuid.UUID) -> Optional[JWTRefreshToken]:
        raise NotImplementedError

    @abstractmethod
    def next_id(self) -> uuid.UUID:
        raise NotImplementedError
