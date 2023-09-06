from pydantic import BaseModel


class SSOLoginContext(BaseModel):
    pass


class SSOLoginURIRequest(BaseModel):
    redirect_uri: str
    context: SSOLoginContext


class SSOLoginURI(BaseModel):
    uri: str


class SSOLogin(BaseModel):
    authorization_code: str
    redirect_uri: str
    state: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class SSOLoginResult(BaseModel):
    tokens: AuthTokens
    context: SSOLoginContext
