import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.modules.auth.api_key.entities import ApiKey
from domain.modules.auth.api_key.repositories import IApiKeyRepository
from .data_mappers import ApiKeyDataMapper
from .models import ApiKeyModel


class ApiKeyRepository(IApiKeyRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_app_id(self, app_id: uuid.UUID) -> Optional[ApiKey]:
        app_api_key_model = self.session.query(ApiKeyModel).filter_by(app_id=app_id).one_or_none()
        if app_api_key_model:
            return ApiKeyDataMapper.model_to_entity(app_api_key_model)
        return None

    def add(self, app_api_key: ApiKey) -> ApiKey:
        app_api_key_model = ApiKeyDataMapper.entity_to_model(app_api_key)
        self.session.add(app_api_key_model)
        self.session.commit()
        return ApiKeyDataMapper.model_to_entity(app_api_key_model)

    def remove(self, app_id: uuid.UUID) -> Optional[ApiKey]:
        app_api_key_model = self.session.query(ApiKeyModel).filter_by(app_id=app_id).one_or_none()
        if not app_api_key_model:
            return None
        self.session.delete(app_api_key_model)
        self.session.commit()
        return ApiKeyDataMapper.model_to_entity(app_api_key_model)
