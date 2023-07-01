import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from domain.app_auth.usecases import AppApiKeyUseCase
from domain.app.entities import App
from domain.app.usecases import AppUseCase
from domain.errors import DomainError
from .use_cases import get_app_api_key_use_case, get_app_use_case

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_app_id(
        api_key: Annotated[str, Depends(api_key_scheme)],
        app_api_key_use_case: Annotated[AppApiKeyUseCase, Depends(get_app_api_key_use_case)],
) -> uuid.UUID | None:
    if not api_key:
        return None
    try:
        return app_api_key_use_case.authenticate_app(api_key)
    except DomainError:
        return None


def get_current_app(
        app_id: Annotated[uuid.UUID, Depends(get_current_app_id)],
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
) -> App | None:
    if not app_id:
        return None
    try:
        return app_use_case.get_by_id(app_id)
    except DomainError:
        return None
