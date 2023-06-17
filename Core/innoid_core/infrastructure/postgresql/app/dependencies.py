from typing import Iterator

from domain.app.usecases import AppUseCase
from .repositories import AppRepository
from ..database import SessionLocal


def get_app_use_case() -> Iterator[AppUseCase]:
    session = SessionLocal()
    try:
        yield AppUseCase(AppRepository(session))
    finally:
        session.close()
