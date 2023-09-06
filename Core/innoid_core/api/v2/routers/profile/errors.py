from fastapi import status

from api.v2.errors import ApiError


class NotAuthenticatedApiError(ApiError):
    error_message = "Not authenticated"
    error_code = 0
    http_status_code = status.HTTP_401_UNAUTHORIZED


class UserNotFoundApiError(ApiError):
    error_message = "User not found"
    error_code = 0
    http_status_code = status.HTTP_404_NOT_FOUND


class ConnectionNotFoundError(ApiError):
    error_message = "Connection not found"
    error_code = 0
    http_status_code = status.HTTP_404_NOT_FOUND
