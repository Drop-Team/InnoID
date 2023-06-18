from typing import Iterator

from domain.identity.usecases import SsoIdentityUseCase


def get_sso_identity_use_case() -> Iterator[SsoIdentityUseCase]:
    yield SsoIdentityUseCase()
