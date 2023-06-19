import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.permission.entities import Permission, UserPermission
from domain.permission.repositories import IUserPermissionRepository, IAppPermissionRepository
from .data_mappers import UserPermissionDataMapper
from .models import UserPermissionModel


class UserPermissionRepository(IUserPermissionRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_user_permissions(self, user_id: uuid.UUID) -> list[UserPermission]:
        user_permission_models = self.session.query(UserPermissionModel).filter_by(user_id=user_id).all()
        return list(map(UserPermissionDataMapper.model_to_entity, user_permission_models))

    def add(self, user_permission: UserPermission) -> UserPermission:
        user_permission_model = UserPermissionDataMapper.entity_to_model(user_permission)
        self.session.add(user_permission_model)
        self.session.commit()
        return UserPermissionDataMapper.model_to_entity(user_permission_model)

    def remove(self, user_id: uuid.UUID, permission: Permission) -> Optional[UserPermission]:
        user_permission_model = self.session.query(UserPermissionModel).filter_by(user_id=user_id,
                                                                                  permission=permission).one_or_none()
        if not user_permission_model:
            return None
        self.session.delete(user_permission_model)
        self.session.commit()
        return UserPermissionDataMapper.model_to_entity(user_permission_model)


class AppPermissionRepository(IAppPermissionRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_app_permissions(self, app_id: uuid.UUID) -> list[UserPermission]:
        app_permission_models = self.session.query(UserPermissionModel).filter_by(app_id=app_id).all()
        return list(map(UserPermissionDataMapper.model_to_entity, app_permission_models))

    def add(self, app_permission: UserPermission) -> UserPermission:
        app_permission_model = UserPermissionDataMapper.entity_to_model(app_permission)
        self.session.add(app_permission_model)
        self.session.commit()
        return UserPermissionDataMapper.model_to_entity(app_permission_model)

    def remove(self, app_id: uuid.UUID, permission: Permission) -> Optional[UserPermission]:
        app_permission_model = self.session.query(UserPermissionModel).filter_by(app_id=app_id,
                                                                                 permission=permission).one_or_none()
        if not app_permission_model:
            return None
        self.session.delete(app_permission_model)
        self.session.commit()
        return UserPermissionDataMapper.model_to_entity(app_permission_model)
