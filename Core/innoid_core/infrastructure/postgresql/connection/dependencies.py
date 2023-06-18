from typing import Iterator

from domain.connection.usecases import TelegramConnectionUseCase
from .repositories import TelegramConnectionRepository
from ..database import SessionLocal


def get_telegram_connection_use_case() -> Iterator[TelegramConnectionUseCase]:
    session = SessionLocal()
    try:
        yield TelegramConnectionUseCase(TelegramConnectionRepository(session))
    finally:
        session.close()
