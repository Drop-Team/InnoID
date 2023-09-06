from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.v2.dependencies.use_cases import get_auth_jwt_use_case
from domain.modules.auth.jwt.usecases import AuthJWTUseCase
from domain.errors import DomainError
from ..common import AuthMethodResult

bearer_scheme = HTTPBearer(auto_error=False)


def get_jwt_auth_result(
        auth_jwt_use_case: Annotated[AuthJWTUseCase, Depends(get_auth_jwt_use_case)],
        access_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> AuthMethodResult:
    user_id = None
    if access_token:
        try:
            user_id = auth_jwt_use_case.authenticate_user(access_token.credentials)
        except DomainError:
            pass
    return AuthMethodResult(
        user_id=user_id,
        app_id=None,
    )
