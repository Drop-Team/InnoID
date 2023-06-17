from typing import Iterator

from domain.user.usecases import UserUseCase
from .repositories import UserRepository
from ..database import SessionLocal


def get_user_use_case() -> Iterator[UserUseCase]:
    session = SessionLocal()
    try:
        yield UserUseCase(UserRepository(session))
    finally:
        session.close()
