import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.modules.role.entities import Role, UserRole
from domain.modules.role.repositories import IUserRoleRepository, IAppRoleRepository
from .data_mappers import UserRoleDataMapper
from .models import UserRoleModel


class UserRoleRepository(IUserRoleRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_user_roles(self, user_id: uuid.UUID) -> list[UserRole]:
        user_role_models = self.session.query(UserRoleModel).filter_by(user_id=user_id).all()
        return list(map(UserRoleDataMapper.model_to_entity, user_role_models))

    def add(self, user_role: UserRole) -> UserRole:
        user_role_model = UserRoleDataMapper.entity_to_model(user_role)
        self.session.add(user_role_model)
        self.session.commit()
        return UserRoleDataMapper.model_to_entity(user_role_model)

    def remove(self, user_id: uuid.UUID, role: Role) -> Optional[UserRole]:
        user_role_model = self.session.query(UserRoleModel).filter_by(user_id=user_id,
                                                                      role=role).one_or_none()
        if not user_role_model:
            return None
        self.session.delete(user_role_model)
        self.session.commit()
        return UserRoleDataMapper.model_to_entity(user_role_model)


class AppRoleRepository(IAppRoleRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_app_roles(self, app_id: uuid.UUID) -> list[UserRole]:
        app_role_models = self.session.query(UserRoleModel).filter_by(app_id=app_id).all()
        return list(map(UserRoleDataMapper.model_to_entity, app_role_models))

    def add(self, app_role: UserRole) -> UserRole:
        app_permission_model = UserRoleDataMapper.entity_to_model(app_role)
        self.session.add(app_permission_model)
        self.session.commit()
        return UserRoleDataMapper.model_to_entity(app_permission_model)

    def remove(self, app_id: uuid.UUID, role: Role) -> Optional[UserRole]:
        app_role_model = self.session.query(UserRoleModel).filter_by(app_id=app_id,
                                                                     role=role).one_or_none()
        if not app_role_model:
            return None
        self.session.delete(app_role_model)
        self.session.commit()
        return UserRoleDataMapper.model_to_entity(app_role_model)
