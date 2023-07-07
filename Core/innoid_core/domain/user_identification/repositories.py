import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import UserCodeIdentification


class IUserCodeIdentificationRepository(ABC):
    @abstractmethod
    def get_by_code(self, code: int) -> Optional[UserCodeIdentification]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_code_identification: UserCodeIdentification) -> UserCodeIdentification:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user_code_identification_id: uuid.UUID) -> Optional[UserCodeIdentification]:
        raise NotImplementedError
