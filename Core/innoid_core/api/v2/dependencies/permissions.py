import uuid
from typing import Annotated

from fastapi import Depends

from api.v2.dependencies.use_cases import get_user_permission_use_case, get_app_permission_use_case
from api.v2.errors import NotPermittedApiError
from domain.permission.entities import Permission
from domain.permission.usecases import UserPermissionUseCase, AppPermissionUseCase
from .apps import get_current_app_id
from .users import get_current_user_id


class PermissionsChecker:
    def __init__(self, permissions: list[Permission]):
        self.permissions: list[Permission] = permissions
        self.admin: bool = Permission.ADMIN in self.permissions

    def check(self, permission: Permission) -> bool:
        return self.admin or permission in self.permissions

    def check_and_raise_error(self, permission: Permission) -> None:
        if not self.check(permission):
            raise NotPermittedApiError()


def get_permissions_checker(
        app_id: Annotated[uuid.UUID | None, Depends(get_current_app_id)],
        user_id: Annotated[uuid.UUID | None, Depends(get_current_user_id)],
        app_permission_use_case: Annotated[AppPermissionUseCase, Depends(get_app_permission_use_case)],
        user_permission_use_case: Annotated[UserPermissionUseCase, Depends(get_user_permission_use_case)],
) -> PermissionsChecker:
    permissions = []
    if app_id:
        permissions = app_permission_use_case.get_app_permissions(app_id)
    elif user_id:
        permissions = user_permission_use_case.get_user_permissions(user_id)
    return PermissionsChecker(permissions)
