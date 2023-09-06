from domain.errors import DomainError


class NotAuthenticatedError(DomainError):
    pass


class RefreshTokenNotFoundError(DomainError):
    pass


class AccessTokenExpiredError(DomainError):
    pass


class RefreshTokenExpiredError(DomainError):
    pass
