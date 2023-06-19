from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from domain.api_key.usecases import AppApiKeyUseCase
from domain.app.entities import App
from domain.app.usecases import AppUseCase
from domain.errors import DomainError
from .use_cases import get_app_api_key_use_case, get_app_use_case

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_app(
        api_key: Annotated[str, Depends(api_key_scheme)],
        app_api_key_use_case: Annotated[AppApiKeyUseCase, Depends(get_app_api_key_use_case)],
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
) -> App | None:
    try:
        app_id = app_api_key_use_case.authenticate(api_key)
        return app_use_case.get_by_id(app_id)
    except DomainError:
        return None
