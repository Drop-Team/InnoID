import uuid
from abc import ABC, abstractmethod
from typing import Optional

from .entities import Permission, UserPermission, AppPermission


class IUserPermissionRepository(ABC):
    @abstractmethod
    def get_user_permissions(self, user_id: uuid.UUID) -> list[UserPermission]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_permission: UserPermission) -> UserPermission:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user_id: uuid.UUID, permission: Permission) -> Optional[UserPermission]:
        raise NotImplementedError


class IAppPermissionRepository(ABC):
    @abstractmethod
    def get_app_permissions(self, app_id: uuid.UUID) -> list[AppPermission]:
        raise NotImplementedError

    @abstractmethod
    def add(self, app_permission: AppPermission) -> AppPermission:
        raise NotImplementedError

    @abstractmethod
    def remove(self, app_id: uuid.UUID, permission: Permission) -> Optional[AppPermission]:
        raise NotImplementedError
