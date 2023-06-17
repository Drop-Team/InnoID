from fastapi import status

from ..errors import ApiError


class UserNotFoundApiError(ApiError):
    error_message = "User not found"
    error_code = 101
    http_status_code = status.HTTP_404_NOT_FOUND
