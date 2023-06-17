from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from .errors import ApiError, InternalApiError


class ExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e, ApiError):
                error = e
            else:
                print(e)
                error = InternalApiError()
            return JSONResponse(
                status_code=error.get_http_status_code(),
                content={"error": error.get_body()},
            )
