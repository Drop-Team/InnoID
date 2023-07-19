from __future__ import annotations

import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from config import Config
from .entities import UserRefreshToken
from .errors import NotAuthenticatedError, RefreshTokenNotFoundError, RefreshTokenExpiredError, AccessTokenExpiredError
from .repositories import IUserRefreshTokenRepository

ACCESS_TOKEN_EXPIRATION = timedelta(minutes=300)
REFRESH_TOKEN_EXPIRATION = timedelta(days=30)


@dataclass
class Tokens:
    access_token: str
    refresh_token: str


class RefreshTokenData:
    def __init__(self, token_id: uuid.UUID, secret: str = None):
        self.token_id = token_id

        if secret is None:
            secret = secrets.token_hex(16)
        self.secret = secret

    @property
    def original_value(self):
        return self.token_id.hex + self.secret

    @property
    def hashed_value(self):
        return pbkdf2_sha256.hash(self.original_value)

    def validate(self, hashed_value: str) -> bool:
        return pbkdf2_sha256.verify(self.original_value, hashed_value)

    @classmethod
    def from_original_refresh_token(cls, original_refresh_token: str) -> RefreshTokenData:
        return RefreshTokenData(
            token_id=uuid.UUID(original_refresh_token[:32]),
            secret=original_refresh_token[32:],
        )


class UserTokenUseCase:
    def __init__(self, user_jwt_refresh_token_repository: IUserRefreshTokenRepository):
        self.user_refresh_token_repository = user_jwt_refresh_token_repository

    def authenticate_user(self, access_token: str) -> uuid.UUID:
        if not access_token:
            raise NotAuthenticatedError()
        try:
            payload = jwt.decode(jwt=access_token, key=Config.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            raise NotAuthenticatedError()
        except jwt.exceptions.ExpiredSignatureError:
            raise AccessTokenExpiredError()
        return uuid.UUID(payload["user_id"])

    def _generate_tokens(self, user_id: uuid.UUID) -> Tokens:
        access_token_payload = {
            "user_id": str(user_id),
            "exp": datetime.now(tz=timezone.utc) + ACCESS_TOKEN_EXPIRATION,
        }
        access_token = jwt.encode(payload=access_token_payload, key=Config.JWT_SECRET_KEY, algorithm="HS256")

        token_id = self.user_refresh_token_repository.next_id()
        refresh_token_data = RefreshTokenData(token_id=token_id)
        refresh_token_entity = UserRefreshToken(
            token_id=token_id,
            user_id=user_id,
            hashed_value=refresh_token_data.hashed_value,
            expires=datetime.now(tz=timezone.utc) + REFRESH_TOKEN_EXPIRATION,
        )
        self.user_refresh_token_repository.add(refresh_token_entity)
        return Tokens(access_token=access_token, refresh_token=refresh_token_data.original_value)

    def create_tokens(self, user_id: uuid.UUID) -> Tokens:
        return self._generate_tokens(user_id)

    def refresh_tokens(self, original_refresh_token: str) -> Tokens:
        if not original_refresh_token or len(original_refresh_token) != 64:
            raise NotAuthenticatedError()
        refresh_token_data = RefreshTokenData.from_original_refresh_token(original_refresh_token)
        refresh_token_entity = self.user_refresh_token_repository.get_by_id(refresh_token_data.token_id)
        if not refresh_token_entity:
            raise RefreshTokenNotFoundError()
        if refresh_token_entity.expires < datetime.now(tz=timezone.utc):
            raise RefreshTokenExpiredError()
        if not refresh_token_data.validate(refresh_token_entity.hashed_value):
            raise NotAuthenticatedError()
        self.user_refresh_token_repository.remove(refresh_token_entity.token_id)

        return self._generate_tokens(refresh_token_entity.user_id)
