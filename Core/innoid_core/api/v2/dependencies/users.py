from typing import Annotated

from fastapi import Depends

from api.v2.dependencies.use_cases import get_user_use_case
from domain.user.entities import User
from domain.user.usecases import UserUseCase


def get_current_user(
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
) -> User | None:
    return None
