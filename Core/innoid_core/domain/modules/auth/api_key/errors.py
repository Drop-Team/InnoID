from domain.errors import DomainError


class NotAuthenticatedError(DomainError):
    pass


class ApiKeyNotFoundError(DomainError):
    pass


class ApiKeyAlreadyExistsError(DomainError):
    pass
