import uuid
from typing import Annotated

from fastapi import Depends

from api.v2.dependencies.use_cases import get_user_use_case
from domain.errors import DomainError
from domain.user.entities import User
from domain.user.usecases import UserUseCase


def get_current_user_id(

) -> uuid.UUID | None:
    return None


def get_current_user(
        user_id: Annotated[uuid.UUID | None, Depends(get_current_user_id)],
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
) -> User | None:
    try:
        return user_use_case.get_by_id(user_id)
    except DomainError:
        return None
