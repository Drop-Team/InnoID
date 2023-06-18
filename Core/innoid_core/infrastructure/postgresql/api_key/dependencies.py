from typing import Iterator

from domain.api_key.usecases import AppApiKeyUseCase
from .repositories import AppApiKeyRepository
from ..database import SessionLocal


def get_app_api_key_use_case() -> Iterator[AppApiKeyUseCase]:
    session = SessionLocal()
    try:
        yield AppApiKeyUseCase(AppApiKeyRepository(session))
    finally:
        session.close()
