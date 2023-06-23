from __future__ import annotations

import uuid
import secrets
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from .entities import AppApiKey
from .errors import ApiKeyNotFoundError, ApiKeyAlreadyExistsError, NotAuthenticatedError
from .repositories import IAppApiKeyRepository


def generate_api_key(app_id: uuid.UUID) -> str:
    secret = secrets.token_hex(16)
    return app_id.hex + secret


def hash_api_key(api_key: str) -> str:
    return pbkdf2_sha256.hash(api_key)


class ApiKeyData:
    def __init__(self, app_id: uuid.UUID, secret: str = None):
        self.app_id = app_id

        if secret is None:
            secret = secrets.token_hex(16)
        self.secret = secret

    @property
    def original_value(self):
        return self.app_id.hex + self.secret

    @property
    def hashed_value(self):
        return pbkdf2_sha256.hash(self.original_value)

    def validate(self, hashed_value: str) -> bool:
        return pbkdf2_sha256.verify(self.original_value, hashed_value)

    @classmethod
    def from_original_api_key(cls, original_api_key: str) -> ApiKeyData:
        return ApiKeyData(
            app_id=uuid.UUID(original_api_key[:32]),
            secret=original_api_key[32:],
        )


class AppApiKeyUseCase:
    app_api_key_repository: IAppApiKeyRepository

    def __init__(self, app_api_key_repository: IAppApiKeyRepository):
        self.app_api_key_repository = app_api_key_repository

    def authenticate_app(self, original_api_key: str) -> uuid.UUID:
        if not original_api_key or len(original_api_key) != 64:
            raise NotAuthenticatedError()
        api_key_data = ApiKeyData.from_original_api_key(original_api_key)
        app_api_key = self.app_api_key_repository.get_by_app_id(api_key_data.app_id)
        if not app_api_key:
            raise NotAuthenticatedError()
        if not api_key_data.validate(app_api_key.hashed_value):
            raise NotAuthenticatedError()
        return app_api_key.app_id

    def _generate_api_key(self, app_id: uuid.UUID) -> str:
        api_key_data = ApiKeyData(app_id=app_id)
        app_api_key = AppApiKey(
            app_id=app_id,
            hashed_value=api_key_data.hashed_value,
            created=datetime.now(),
        )
        self.app_api_key_repository.add(app_api_key)
        return api_key_data.original_value

    def create_api_key(self, app_id: uuid.UUID) -> str:
        app_api_key = self.app_api_key_repository.get_by_app_id(app_id)
        if app_api_key:
            raise ApiKeyAlreadyExistsError()
        return self._generate_api_key(app_id)

    def refresh_api_key(self, app_id: uuid.UUID) -> str:
        app_api_key = self.app_api_key_repository.get_by_app_id(app_id)
        if not app_api_key:
            raise ApiKeyNotFoundError()
        self.app_api_key_repository.remove(app_id)

        return self._generate_api_key(app_id)
