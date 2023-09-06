from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from api.v2.dependencies.use_cases import get_auth_api_key_use_case
from domain.modules.auth.api_key.usecases import AuthApiKeyUseCase
from domain.errors import DomainError
from ..common import AuthMethodResult

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key_auth_result(
        api_key: Annotated[str, Depends(api_key_scheme)],
        auth_api_key_use_case: Annotated[AuthApiKeyUseCase, Depends(get_auth_api_key_use_case)],
) -> AuthMethodResult:
    app_id = None
    if api_key:
        try:
            app_id = auth_api_key_use_case.authenticate_app(api_key)
        except DomainError:
            pass
    return AuthMethodResult(
        user_id=None,
        app_id=app_id,
    )
