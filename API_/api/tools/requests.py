from functools import wraps

from flask import request

from api.database.db_session import create_session
from api.models.apps import App
from api.tools import errors
from api.tools.metrics import apps_requests


def get_token(auth: str) -> str:
    auth_parts = auth.split()
    if len(auth_parts) == 2 and auth_parts[0] == "Bearer":
        return auth_parts[1]
    return None


def get_app_by_token(token: str) -> App:
    session = create_session()
    app = session.query(App).filter(App.token == token).first()
    return app


def auth_check(required_permission: int):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            token = get_token(request.headers.get("Authorization", ""))
            app = get_app_by_token(token) if token else None
            if not token or not app:
                raise errors.NoAuthError

            metric_labels = [app.id, app.name, request.path]

            if required_permission not in decode_number(app.api_permissions):
                apps_requests.labels(*metric_labels, "Access denied").inc()
                raise errors.AccessDeniedError

            apps_requests.labels(*metric_labels, "Success").inc()
            return func(*args, **kwargs, user_fields=decode_number(app.allowed_user_fields))

        return decorator

    return wrapper


def decode_number(number: int) -> list[int]:
    result = []
    for i, digit in enumerate(bin(number)[::-1]):
        if digit == "b":
            return result
        if digit == "1":
            result.append(i + 1)
    return result


def encode_numbers(numbers: list[int]) -> int:
    if not numbers:
        return 0
    length = max(numbers)
    result = ["0"] * length
    for num in numbers:
        result[length - num - 1] = "1"

    encoded_number = int("".join(result), 2)
    return encoded_number
