import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.use_cases import get_user_use_case
from api.v2.dependencies.users import get_current_user
from domain.user import errors as domain_errors
from domain.user.entities import User
from domain.user.usecases import UserUseCase
from . import errors as api_errors
from . import models as api_models

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=api_models.User)
def get_current_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise api_errors.UserNotFoundApiError()
    return api_models.User(user_id=user.user_id, email=user.email)


@users_router.get("/{user_id}", response_model=api_models.User)
def get_user(
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
        user_id: uuid.UUID
):
    try:
        user = user_use_case.get_by_id(user_id)
        return api_models.User(user_id=user.user_id, email=user.email)
    except domain_errors.UserNotFoundError:
        raise api_errors.UserNotFoundApiError()


@users_router.post("", response_model=api_models.User)
def create_user(
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
        user_email_model: api_models.UserCreate,
):
    user = user_use_case.create(email=user_email_model.email)
    return api_models.User(user_id=user.user_id, email=user.email)
