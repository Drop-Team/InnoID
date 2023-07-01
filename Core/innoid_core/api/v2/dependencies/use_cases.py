from typing import Iterator

from domain.app.usecases import AppUseCase
from domain.app_auth.usecases import AppApiKeyUseCase
from domain.connection.usecases import TelegramConnectionUseCase
from domain.identity.usecases import SsoIdentityUseCase
from domain.permission.usecases import UserPermissionUseCase, AppPermissionUseCase
from domain.user.usecases import UserUseCase
from domain.user_auth.usecases import UserTokenUseCase
from infrastructure.postgresql.app.repositories import AppRepository
from infrastructure.postgresql.app_auth.repositories import AppApiKeyRepository
from infrastructure.postgresql.connection.repositories import TelegramConnectionRepository
from infrastructure.postgresql.database import SessionLocal
from infrastructure.postgresql.permission.repositories import UserPermissionRepository, AppPermissionRepository
from infrastructure.postgresql.user.repositories import UserRepository
from infrastructure.postgresql.user_auth.repositories import UserRefreshTokenRepository


def get_user_use_case() -> Iterator[UserUseCase]:
    session = SessionLocal()
    try:
        yield UserUseCase(UserRepository(session))
    finally:
        session.close()


def get_app_use_case() -> Iterator[AppUseCase]:
    session = SessionLocal()
    try:
        yield AppUseCase(AppRepository(session))
    finally:
        session.close()


def get_user_permission_use_case() -> Iterator[UserPermissionUseCase]:
    session = SessionLocal()
    try:
        yield UserPermissionUseCase(UserPermissionRepository(session))
    finally:
        session.close()


def get_app_permission_use_case() -> Iterator[AppPermissionUseCase]:
    session = SessionLocal()
    try:
        yield AppPermissionUseCase(AppPermissionRepository(session))
    finally:
        session.close()


def get_telegram_connection_use_case() -> Iterator[TelegramConnectionUseCase]:
    session = SessionLocal()
    try:
        yield TelegramConnectionUseCase(TelegramConnectionRepository(session))
    finally:
        session.close()


def get_sso_identity_use_case() -> Iterator[SsoIdentityUseCase]:
    yield SsoIdentityUseCase()


def get_app_api_key_use_case() -> Iterator[AppApiKeyUseCase]:
    session = SessionLocal()
    try:
        yield AppApiKeyUseCase(AppApiKeyRepository(session))
    finally:
        session.close()


def get_user_token_use_case() -> Iterator[UserTokenUseCase]:
    session = SessionLocal()
    try:
        yield UserTokenUseCase(UserRefreshTokenRepository(session))
    finally:
        session.close()
