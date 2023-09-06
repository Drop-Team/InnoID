from typing import Annotated

from fastapi import APIRouter, Depends

from api.v2.dependencies.use_cases import get_auth_jwt_use_case
from api.v2.dependencies.use_cases import get_login_sso_use_case
from api.v2.dependencies.use_cases import get_user_use_case
from domain.modules.auth.jwt.usecases import AuthJWTUseCase
from domain.modules.login.sso.usecases import LoginSSOUseCase
from domain.modules.user.errors import UserNotFoundError
from domain.modules.user.usecases import UserUseCase
from . import models as api_models

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post("/sso/uri", response_model=api_models.SSOLoginURI)
def get_sso_login_uri(
        login_sso_use_case: Annotated[LoginSSOUseCase, Depends(get_login_sso_use_case)],
        sso_login_uri_request: api_models.SSOLoginURIRequest
):
    uri = login_sso_use_case.get_login_uri(
        redirect_uri=sso_login_uri_request.redirect_uri,
        context=sso_login_uri_request.context.dict()
    )
    return api_models.SSOLoginURI(uri=uri)


@login_router.post("/sso/login", response_model=api_models.SSOLoginResult)
def login_with_sso(
        login_sso_use_case: Annotated[LoginSSOUseCase, Depends(get_login_sso_use_case)],
        auth_jwt_use_case: Annotated[AuthJWTUseCase, Depends(get_auth_jwt_use_case)],
        user_use_case: Annotated[UserUseCase, Depends(get_user_use_case)],
        sso_login: api_models.SSOLogin,
):
    sso_login_result = login_sso_use_case.get_user_info(
        code=sso_login.authorization_code,
        redirect_uri=sso_login.redirect_uri,
        state=sso_login.state,
    )
    context = api_models.SSOLoginContext(**sso_login_result.context)

    try:
        user = user_use_case.get_by_email(email=sso_login_result.user_info.email)
    except UserNotFoundError:
        user = user_use_case.create(email=sso_login_result.user_info.email)

    tokens = auth_jwt_use_case.create_tokens(user_id=user.user_id)

    login_result = api_models.SSOLoginResult(
        tokens=api_models.AuthTokens(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        ),
        context=context,
    )
    return login_result
