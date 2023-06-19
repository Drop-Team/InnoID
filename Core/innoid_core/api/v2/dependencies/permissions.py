from typing import Annotated

from fastapi import Depends

from api.v2.dependencies.use_cases import get_user_permission_use_case, get_app_permission_use_case
from domain.app.entities import App
from domain.permission.entities import Permission
from domain.permission.usecases import UserPermissionUseCase, AppPermissionUseCase
from domain.user.entities import User
from .apps import get_current_app
from .users import get_current_user


class PermissionsChecker:
    def __init__(self, permissions: list[Permission]):
        self.permissions: list[Permission] = permissions
        self.admin: bool = Permission.ADMIN in self.permissions

    def check(self, permission: Permission) -> bool:
        return self.admin or permission in self.permissions


def get_permissions_checker(
        app: Annotated[App | None, Depends(get_current_app)],
        user: Annotated[User | None, Depends(get_current_user)],
        app_permission_use_case: Annotated[AppPermissionUseCase, Depends(get_app_permission_use_case)],
        user_permission_use_case: Annotated[UserPermissionUseCase, Depends(get_user_permission_use_case)],
) -> PermissionsChecker:
    permissions = []
    if app:
        permissions = app_permission_use_case.get_app_permissions(app.app_id)
    elif user:
        permissions = user_permission_use_case.get_user_permissions(user.user_id)
    return PermissionsChecker(permissions)
