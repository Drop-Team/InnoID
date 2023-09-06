import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.modules.app.entities import App
from domain.modules.app.repositories import IAppRepository
from .data_mappers import AppDataMapper
from .models import AppModel


class AppRepository(IAppRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, app_id: uuid.UUID) -> Optional[App]:
        app_model = self.session.query(AppModel).filter_by(app_id=app_id).one_or_none()
        if app_model:
            return AppDataMapper.model_to_entity(app_model)
        return None

    def get_list(self, offset: int, limit: int) -> list[App]:
        app_models = self.session.query(AppModel).offset(offset).limit(limit).all()
        return list(map(AppDataMapper.model_to_entity, app_models))

    def get_by_owner_id(self, owner_id: uuid.UUID) -> list[App]:
        app_models = self.session.query(AppModel).filter_by(owner_id=owner_id).all()
        return list(map(AppDataMapper.model_to_entity, app_models))

    def add(self, app: App) -> App:
        app_model = AppDataMapper.entity_to_model(app)
        self.session.add(app_model)
        self.session.commit()
        return AppDataMapper.model_to_entity(app_model)

    def remove(self, app_id: uuid.UUID) -> Optional[App]:
        app_model = self.session.query(AppModel).filter_by(app_id=app_id).one_or_none()
        if not app_model:
            return None
        self.session.delete(app_model)
        self.session.commit()
        return AppDataMapper.model_to_entity(app_model)

    def next_id(self) -> uuid.UUID:
        return App.next_id()
