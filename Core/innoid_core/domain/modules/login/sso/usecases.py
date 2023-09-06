from dataclasses import dataclass

from domain.external_users import IExternalUsers
from .errors import RetrievingUserInfoFailedError


@dataclass
class SSOUserInfo:
    email: str
    name: str
    surname: str
    display_name: str
    job: str


@dataclass
class SSOLoginResult:
    context: dict
    user_info: SSOUserInfo


class LoginSSOUseCase:
    external_users: IExternalUsers

    def __init__(self, external_users: IExternalUsers):
        self.external_users = external_users

    def get_login_uri(self, redirect_uri: str, context: dict) -> str:
        return self.external_users.get_oauth_login_uri(redirect_uri, context)

    def get_user_info(self, code: str, state: str, redirect_uri: str) -> SSOLoginResult:
        oauth_result = self.external_users.get_oauth_user_info(code, state, redirect_uri)
        if not oauth_result:
            raise RetrievingUserInfoFailedError()
        return SSOLoginResult(
            context=oauth_result.context,
            user_info=SSOUserInfo(
                email=oauth_result.user_info.email,
                name=oauth_result.user_info.name,
                surname=oauth_result.user_info.surname,
                display_name=oauth_result.user_info.display_name,
                job=oauth_result.user_info.job,
            ),
        )
