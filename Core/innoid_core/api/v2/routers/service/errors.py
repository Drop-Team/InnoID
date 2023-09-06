from fastapi import status

from api.v2.errors import ApiError


class NotAuthenticatedApiError(ApiError):
    error_message = "Not allowed"
    error_code = 0
    http_status_code = status.HTTP_401_UNAUTHORIZED


class InvalidIdCodeApiError(ApiError):
    error_message = "Invalid identification code"
    error_code = 0
    http_status_code = status.HTTP_401_UNAUTHORIZED
