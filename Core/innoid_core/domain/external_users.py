from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ExternalUserInfo:
    email: str
    name: str
    surname: str
    display_name: str
    job: str


@dataclass
class OAuthResult:
    context: dict
    user_info: ExternalUserInfo


class IExternalUsers(ABC):
    @abstractmethod
    def get_oauth_login_uri(self, redirect_uri: str, context: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_oauth_user_info(self, code: str, state: str, redirect_uri: str) -> OAuthResult | None:
        raise NotImplementedError
