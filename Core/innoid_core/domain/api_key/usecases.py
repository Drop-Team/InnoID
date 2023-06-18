import uuid
import secrets
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from .entities import AppApiKey
from .errors import ApiKeyNotFoundError, ApiKeyAlreadyExistsError, NotAuthenticatedError
from .repositories import IAppApiKeyRepository


class ApiKeyData:
    def __init__(self, raw_value: str = None):
        if raw_value:
            self.raw_value = raw_value
        else:
            self.raw_value = secrets.token_hex(16)

    @property
    def hashed_value(self):
        return pbkdf2_sha256.hash(self.raw_value)


class AppApiKeyUseCase:
    app_api_key_repository: IAppApiKeyRepository

    def __init__(self, app_api_key_repository: IAppApiKeyRepository):
        self.app_api_key_repository = app_api_key_repository

    def authenticate(self, api_key_string: str) -> uuid.UUID:
        api_key_data = ApiKeyData(api_key_string)
        app_api_key = self.app_api_key_repository.get_by_hashed_value(api_key_data.hashed_value)
        if not app_api_key:
            raise NotAuthenticatedError()
        return app_api_key.app_id

    def generate(self, app_id: uuid.UUID) -> str:
        app_api_key = self.app_api_key_repository.get_by_app_id(app_id)
        if app_api_key:
            raise ApiKeyAlreadyExistsError()
        api_key_data = ApiKeyData()
        app_api_key = AppApiKey(
            app_id=app_id,
            hashed_value=api_key_data.hashed_value,
            created=datetime.now(),
        )
        self.app_api_key_repository.add(app_api_key)
        return api_key_data.raw_value

    def refresh(self, app_id: uuid.UUID) -> str:
        app_api_key = self.app_api_key_repository.get_by_app_id(app_id)
        if not app_api_key:
            raise ApiKeyNotFoundError()
        self.app_api_key_repository.remove(app_id)

        api_key_data = ApiKeyData()
        app_api_key = AppApiKey(
            app_id=app_id,
            hashed_value=api_key_data.hashed_value,
            created=datetime.now(),
        )
        self.app_api_key_repository.add(app_api_key)
        return api_key_data.raw_value
