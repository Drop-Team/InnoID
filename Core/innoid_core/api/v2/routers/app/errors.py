from fastapi import status

from api.v2.errors import ApiError


class AppNotFoundApiError(ApiError):
    error_message = "App not found"
    error_code = 201
    http_status_code = status.HTTP_404_NOT_FOUND
