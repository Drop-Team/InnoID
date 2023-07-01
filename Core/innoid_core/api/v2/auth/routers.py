from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.use_cases import get_user_token_use_case
from api.v2.dependencies.use_cases import get_user_use_case
from domain.user.errors import UserNotFoundError
from domain.user.usecases import UserUseCase
from domain.user_auth.usecases import UserTokenUseCase
from infrastructure import sso
from . import models as api_models

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/sso/uri", response_model=api_models.SsoLoginURI)
def get_sso_login_uri(
        sso_login_uri_request: api_models.SsoLoginURIRequest
):
    uri = sso.get_uri(
        redirect_uri=sso_login_uri_request.redirect_uri,
        context=sso_login_uri_request.context.dict()
    )
    return api_models.SsoLoginURI(uri=uri)


@auth_router.post("/sso/login", response_model=api_models.SsoLoginResult)
def login_with_sso(
        sso_login: api_models.SsoLogin,
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
        user_token_use_case: Annotated[UserTokenUseCase, Depends(get_user_token_use_case)],
):
    sso_identity_result = sso.get_user_info(
        code=sso_login.authorization_code,
        redirect_uri=sso_login.redirect_uri,
        state=sso_login.state,
    )
    context = api_models.SsoLoginContext(**sso_identity_result.context)

    try:
        user = user_use_case.get_by_email(sso_identity_result.email)
    except UserNotFoundError:
        user = user_use_case.create(email=sso_identity_result.email)

    tokens = user_token_use_case.create_tokens(user_id=user.user_id)

    login_result = api_models.SsoLoginResult(
        tokens=api_models.AuthTokens(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        ),
        context=context,
    )
    return login_result
