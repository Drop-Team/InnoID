import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from domain.app import errors as domain_errors
from domain.app.usecases import AppUseCase
from infrastructure.postgresql.app.dependencies import get_app_use_case
from . import errors as api_errors
from . import models as api_models

apps_router = APIRouter(prefix="/apps", tags=["apps"])


@apps_router.get("/{app_id}", response_model=api_models.App)
def get_app(
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
        app_id: uuid.UUID
):
    try:
        app = app_use_case.get_by_id(app_id)
        return api_models.App(app_id=app.app_id, name=app.name, owner_id=app.owner_id)
    except domain_errors.AppNotFoundError:
        raise api_errors.AppNotFoundApiError()


@apps_router.post("", response_model=api_models.App)
def create_app(
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
        app_create_model: api_models.AppCreate,
):
    app = app_use_case.create(name=app_create_model.name, owner_id=app_create_model.owner_id)
    return api_models.App(app_id=app.app_id, name=app.name, owner_id=app.owner_id)
