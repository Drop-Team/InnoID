import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.app_auth.entities import AppApiKey
from domain.app_auth.repositories import IAppApiKeyRepository
from .data_mappers import AppApiKeyDataMapper
from .models import AppApiKeyModel


class AppApiKeyRepository(IAppApiKeyRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_app_id(self, app_id: uuid.UUID) -> Optional[AppApiKey]:
        app_api_key_model = self.session.query(AppApiKeyModel).filter_by(app_id=app_id).one_or_none()
        if app_api_key_model:
            return AppApiKeyDataMapper.model_to_entity(app_api_key_model)
        return None

    def add(self, app_api_key: AppApiKey) -> AppApiKey:
        app_api_key_model = AppApiKeyDataMapper.entity_to_model(app_api_key)
        self.session.add(app_api_key_model)
        self.session.commit()
        return AppApiKeyDataMapper.model_to_entity(app_api_key_model)

    def remove(self, app_id: uuid.UUID) -> Optional[AppApiKey]:
        app_api_key_model = self.session.query(AppApiKeyModel).filter_by(app_id=app_id).one_or_none()
        if not app_api_key_model:
            return None
        self.session.delete(app_api_key_model)
        self.session.commit()
        return AppApiKeyDataMapper.model_to_entity(app_api_key_model)
