from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.use_cases import get_app_use_case
from api.v2.dependencies.use_cases import get_telegram_connection_use_case
from api.v2.dependencies.users import get_current_user
from domain.app.usecases import AppUseCase
from domain.connection.usecases import TelegramConnectionUseCase
from domain.user.entities import User
from . import errors as api_errors
from . import models as api_models

profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.get("", response_model=api_models.User)
def get_current_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise api_errors.NotAuthenticatedApiError()
    return api_models.User(user_id=user.user_id, email=user.email)


@profile_router.get("/apps", response_model=list[api_models.UserApp])
def get_user_apps(
        user: Annotated[User, Depends(get_current_user)],
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
):
    apps = app_use_case.get_by_owner_id(owner_id=user.user_id)
    return [api_models.UserApp(id=app.app_id, name=app.name) for app in apps]


@profile_router.post("/apps", response_model=api_models.UserApp)
def create_user_app(
        user: Annotated[User, Depends(get_current_user)],
        app_use_case: Annotated[AppUseCase, Depends(get_app_use_case)],
        app_create_model: api_models.UserAppCreate,
):
    app = app_use_case.create(name=app_create_model.name, owner_id=user.user_id)
    return api_models.UserApp(id=app.app_id, name=app.name)


@profile_router.get("/connections/telegram", response_model=api_models.UserTelegramConnection)
def get_user_telegram_connection(
        user: Annotated[User, Depends(get_current_user)],
        telegram_connection_use_case: Annotated[TelegramConnectionUseCase, Depends(get_telegram_connection_use_case)],
):
    telegram_connection = telegram_connection_use_case.get_by_user_id(user_id=user.user_id)
    return api_models.UserTelegramConnection(
        created=telegram_connection.created,
        telegram_id=telegram_connection.telegram_id
    )