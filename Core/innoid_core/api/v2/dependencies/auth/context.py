from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from domain.modules.app.entities import App
from domain.modules.role.entities import Role
from domain.modules.role.usecases import UserRoleUseCase, AppRoleUseCase
from domain.modules.user.entities import User
from .subject import AuthenticationSubject, get_authentication_subject
from ..use_cases import get_user_role_use_case, get_app_role_use_case
from ...errors import NotPermittedApiError


@dataclass
class AuthContext:
    user: User | None
    app: App | None
    roles: list[Role]


class AuthContextProvider:
    def __init__(self, *required_roles: Role):
        self._required_roles = required_roles

    def check_roles(
            self,
            roles: list[Role],
            is_app: bool,
            is_user: bool,
    ) -> bool:
        if Role.USER in self._required_roles and not is_user:
            return False
        if Role.APP in self._required_roles and not is_app:
            return False
        if Role.ADMIN in roles:
            return True
        for required_permission in self._required_roles:
            if required_permission not in roles:
                return False
        return True

    def __call__(
            self,
            app_role_use_case: Annotated[AppRoleUseCase, Depends(get_app_role_use_case)],
            user_role_use_case: Annotated[UserRoleUseCase, Depends(get_user_role_use_case)],
            auth_subject: Annotated[AuthenticationSubject, Depends(get_authentication_subject)],
    ) -> AuthContext:
        roles = []
        is_user = False
        is_app = False
        if auth_subject.user:
            roles = user_role_use_case.get_user_roles(auth_subject.user.user_id)
            is_user = True
        elif auth_subject.app:
            roles = app_role_use_case.get_app_roles(auth_subject.app.app_id)
            is_app = True
        if not self.check_roles(roles, is_app, is_user):
            raise NotPermittedApiError()
        return AuthContext(
            user=auth_subject.user,
            app=auth_subject.app,
            roles=roles,
        )
