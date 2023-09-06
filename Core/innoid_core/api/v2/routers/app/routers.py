import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.auth import AuthContext, AuthContextProvider
from api.v2.dependencies.use_cases import get_app_use_case, get_auth_api_key_use_case
from domain.modules.app import errors as domain_errors
from domain.modules.app.usecases import AppUseCase
from domain.modules.auth.api_key.usecases import AuthApiKeyUseCase
from domain.modules.role.entities import Role
from . import errors as api_errors
from . import models as api_models

apps_router = APIRouter(prefix="/apps", tags=["apps"])


@apps_router.get("/me", response_model=api_models.App)
def get_current_active_app(
        auth_context: Annotated[AuthContext, Depends(AuthContextProvider(Role.APP))]
):
    app = auth_context.app
    return api_models.App(app_id=app.app_id, name=app.name, owner_id=app.owner_id)


@apps_router.get("/{app_id}", response_model=api_models.App)
def get_app(
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
        app_id: uuid.UUID,
):
    try:
        app = app_use_case.get_by_id(app_id)
    except domain_errors.AppNotFoundError:
        raise api_errors.AppNotFoundApiError()
    return api_models.App(app_id=app.app_id, name=app.name, owner_id=app.owner_id)


@apps_router.post("", response_model=api_models.AppWithApiKey)
def create_app(
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
        auth_api_key_use_case: Annotated[AuthApiKeyUseCase, Depends(get_auth_api_key_use_case)],
        app_create_model: api_models.AppCreate,
):
    app = app_use_case.create(name=app_create_model.name, owner_id=app_create_model.owner_id)
    original_api_key = auth_api_key_use_case.create_api_key(app_id=app.app_id)
    return api_models.AppWithApiKey(app_id=app.app_id, name=app.name, owner_id=app.owner_id, api_key=original_api_key)
