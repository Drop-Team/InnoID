import uuid
from typing import Annotated

from fastapi import Depends

from .auth import get_authentication, Authentication
from api.v2.errors import NotPermittedApiError
from domain.modules.role.entities import Role
from domain.modules.role.usecases import UserRoleUseCase, AppRoleUseCase
from .use_cases import get_app_role_use_case, get_user_role_use_case


class RoleChecker:
    def __init__(self, *required_roles: list[Role]):
        self.required_roles = required_roles

    def __call__(
            self,
            app_permission_use_case: Annotated[AppRoleUseCase, Depends(get_app_role_use_case)],
            user_permission_use_case: Annotated[UserRoleUseCase, Depends(get_user_role_use_case)],
            auth_result: Annotated[Authentication, Depends(get_authentication)],
    ) -> bool:
        permissions = []
        if auth_result.user:
            permissions = user_permission_use_case.get_user_roles(auth_result.user.user_id)
        elif auth_result.app:
            permissions = app_permission_use_case.get_app_roles(auth_result.app.app_id)
        if Role.USER in self.required_roles and Role.USER not in permissions:
            return False
        if Role.APP in self.required_roles and Role.APP not in permissions:
            return False
        if Role.ADMIN in permissions:
            return True
        for required_permission in self.required_roles:
            if required_permission not in permissions:
                return False
        return True


class PermissionsChecker:
    def __init__(self, permissions: list[Role]):
        self.permissions: list[Role] = permissions
        self.admin: bool = Role.ADMIN in self.permissions

    def check(self, permission: Role) -> bool:
        return self.admin or permission in self.permissions

    def check_and_raise_error(self, permission: Role) -> None:
        if not self.check(permission):
            raise NotPermittedApiError()


def get_permissions_checker(
        app_permission_use_case: Annotated[AppRoleUseCase, Depends(get_app_role_use_case)],
        user_permission_use_case: Annotated[UserRoleUseCase, Depends(get_user_role_use_case)],
        auth_result: Annotated[Authentication, Depends(get_authentication)],
) -> PermissionsChecker:
    permissions = []
    if app_id:
        permissions = app_permission_use_case.get_app_roles(app_id)
    elif user_id:
        permissions = user_permission_use_case.get_user_roles(user_id)
    return PermissionsChecker(permissions)
