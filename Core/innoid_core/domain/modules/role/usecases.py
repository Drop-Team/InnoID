import uuid

from .entities import Role, UserRole, AppRole
from .errors import RoleNotFoundError
from .repositories import IUserRoleRepository, IAppRoleRepository


class UserRoleUseCase:
    user_role_repository: IUserRoleRepository

    def __init__(self, user_role_repository: IUserRoleRepository):
        self.user_role_repository = user_role_repository

    def get_user_roles(self, user_id: uuid.UUID) -> list[Role]:
        roles = [Role.USER]
        user_roles = self.user_role_repository.get_user_roles(user_id)
        for user_role in user_roles:
            roles.append(user_role.role)
        return roles

    def add_role(self, user_id: uuid.UUID, role: Role) -> UserRole:
        role = UserRole(user_id=user_id, role=role)
        self.user_role_repository.add(role)
        return role

    def remove_role(self, user_id: uuid.UUID, role: Role) -> UserRole:
        role = self.user_role_repository.remove(user_id, role)
        if not role:
            raise RoleNotFoundError()
        return role


class AppRoleUseCase:
    app_role_repository: IAppRoleRepository

    def __init__(self, app_role_repository: IAppRoleRepository):
        self.app_role_repository = app_role_repository

    def get_app_roles(self, app_id: uuid.UUID) -> list[Role]:
        roles = [Role.APP]
        app_roles = self.app_role_repository.get_app_roles(app_id)
        for app_role in app_roles:
            roles.append(app_role.role)
        return roles

    def add_role(self, app_id: uuid.UUID, role: Role) -> AppRole:
        role = AppRole(app_id=app_id, role=role)
        self.app_role_repository.add(role)
        return role

    def remove_role(self, app_id: uuid.UUID, role: Role) -> AppRole:
        role = self.app_role_repository.remove(app_id, role)
        if not role:
            raise RoleNotFoundError()
        return role
