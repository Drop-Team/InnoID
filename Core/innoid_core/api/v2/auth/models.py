from pydantic import BaseModel


class SsoLoginContext(BaseModel):
    pass


class SsoLoginURIRequest(BaseModel):
    redirect_uri: str
    context: SsoLoginContext


class SsoLoginURI(BaseModel):
    uri: str


class SsoLogin(BaseModel):
    authorization_code: str
    redirect_uri: str
    state: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class SsoLoginResult(BaseModel):
    tokens: AuthTokens
    context: SsoLoginContext
