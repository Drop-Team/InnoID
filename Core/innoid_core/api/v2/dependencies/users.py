import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.v2.dependencies.use_cases import get_user_use_case, get_user_token_use_case
from domain.errors import DomainError
from domain.user.entities import User
from domain.user.usecases import UserUseCase
from domain.user_auth.usecases import UserTokenUseCase


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(
        user_access_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
        user_token_use_case: Annotated[UserTokenUseCase, Depends(get_user_token_use_case)],
) -> uuid.UUID | None:
    if not user_access_token:
        return None
    try:
        return user_token_use_case.authenticate_user(user_access_token.credentials)
    except DomainError:
        return None


def get_current_user(
        user_id: Annotated[uuid.UUID | None, Depends(get_current_user_id)],
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
) -> User | None:
    if not user_id:
        return None
    try:
        return user_use_case.get_by_id(user_id)
    except DomainError:
        return None
