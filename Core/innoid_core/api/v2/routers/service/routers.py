from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.use_cases import (
    get_telegram_connection_use_case,
    get_user_code_identification_use_case
)
from domain.modules.code_identification.errors import IdentificationNotFoundError
from domain.modules.code_identification.usecases import UserCodeIdentificationUseCase
from domain.modules.connection.telegram.usecases import TelegramConnectionUseCase
from . import errors as api_errors
from . import models as api_models

service_router = APIRouter(prefix="/service", tags=["service"])


@service_router.post("/user_id/code", response_model=api_models.UserId)
def get_user_id_by_id_code(
        user_code_identification_use_case: Annotated[
            UserCodeIdentificationUseCase, Depends(get_user_code_identification_use_case)
        ],
        user_id_code: api_models.UserIdCode,
):
    try:
        user_identification = user_code_identification_use_case.get_by_code(code=user_id_code.code)
    except IdentificationNotFoundError:
        raise api_errors.InvalidIdCodeApiError()
    return api_models.UserId(user_id=user_identification.user_id)


@service_router.post("/connections/telegram", response_model=api_models.UserTelegramConnection)
def create_telegram_connection(
        telegram_connection_use_case: Annotated[TelegramConnectionUseCase, Depends(get_telegram_connection_use_case)],
        user_telegram_connection: api_models.UserTelegramConnectionCreate,
):
    telegram_connection = telegram_connection_use_case.create(
        user_id=user_telegram_connection.user_id,
        telegram_id=user_telegram_connection.telegram_id,
    )
    return api_models.UserTelegramConnection(
        created=telegram_connection.created,
        user_id=telegram_connection.user_id,
        telegram_id=telegram_connection.telegram_id,
    )
