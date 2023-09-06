import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import Role, UserRole, AppRole


class IUserRoleRepository(ABC):
    @abstractmethod
    def get_user_roles(self, user_id: uuid.UUID) -> list[UserRole]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_role: UserRole) -> UserRole:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user_id: uuid.UUID, role: Role) -> Optional[UserRole]:
        raise NotImplementedError


class IAppRoleRepository(ABC):
    @abstractmethod
    def get_app_roles(self, app_id: uuid.UUID) -> list[AppRole]:
        raise NotImplementedError

    @abstractmethod
    def add(self, app_role: AppRole) -> AppRole:
        raise NotImplementedError

    @abstractmethod
    def remove(self, app_id: uuid.UUID, role: Role) -> Optional[AppRole]:
        raise NotImplementedError
