from abc import ABC

from starlette import status


class ApiError(ABC, Exception):
    error_message: str = None
    error_code: int = None
    http_status_code: int = None

    def get_body(self) -> dict:
        return {"message": self.error_message, "code": self.error_code}

    def get_http_status_code(self) -> int:
        return self.http_status_code


class InternalApiError(ApiError):
    error_message: str = "Internal error"
    error_code: int = 1
    http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class NotPermittedApiError(ApiError):
    error_message: str = "Not permitted"
    error_code: int = 11
    http_status_code: int = status.HTTP_403_FORBIDDEN
