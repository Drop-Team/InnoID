import uuid

from .entities import Permission, UserPermission, AppPermission
from .errors import PermissionNotFoundError
from .repositories import IUserPermissionRepository, IAppPermissionRepository


class UserPermissionUseCase:
    user_permission_repository: IUserPermissionRepository

    def __init__(self, user_permission_repository: IUserPermissionRepository):
        self.user_permission_repository = user_permission_repository

    def get_user_permissions(self, user_id: uuid.UUID) -> list[Permission]:
        permissions = [Permission.USER]
        user_permissions = self.user_permission_repository.get_user_permissions(user_id)
        for user_permission in user_permissions:
            permissions.append(user_permission.permission)
        return permissions

    def add_permission(self, user_id: uuid.UUID, permission: Permission) -> UserPermission:
        permission = UserPermission(user_id=user_id, permission=permission)
        self.user_permission_repository.add(permission)
        return permission

    def remove_permission(self, user_id: uuid.UUID, permission: Permission) -> UserPermission:
        permission = self.user_permission_repository.remove(user_id, permission)
        if not permission:
            raise PermissionNotFoundError()
        return permission


class AppPermissionUseCase:
    app_permission_repository: IAppPermissionRepository

    def __init__(self, app_permission_repository: IAppPermissionRepository):
        self.app_permission_repository = app_permission_repository

    def get_app_permissions(self, app_id: uuid.UUID) -> list[Permission]:
        permissions = [Permission.APP]
        app_permissions = self.app_permission_repository.get_app_permissions(app_id)
        for app_permission in app_permissions:
            permissions.append(app_permission.permission)
        return permissions

    def add_permission(self, app_id: uuid.UUID, permission: Permission) -> AppPermission:
        permission = AppPermission(app_id=app_id, permission=permission)
        self.app_permission_repository.add(permission)
        return permission

    def remove_permission(self, app_id: uuid.UUID, permission: Permission) -> AppPermission:
        permission = self.app_permission_repository.remove(app_id, permission)
        if not permission:
            raise PermissionNotFoundError()
        return permission
