from domain.permission.entities import UserPermission, AppPermission
from .models import UserPermissionModel, AppPermissionModel


class UserPermissionDataMapper:
    @staticmethod
    def model_to_entity(model: UserPermissionModel) -> UserPermission:
        return UserPermission(
            user_id=model.user_id,
            permission=model.permission,
        )

    @staticmethod
    def entity_to_model(entity: UserPermission) -> UserPermissionModel:
        return UserPermissionModel(
            user_id=entity.user_id,
            permission=entity.permission,
        )


class AppPermissionDataMapper:
    @staticmethod
    def model_to_entity(model: AppPermissionModel) -> AppPermission:
        return AppPermission(
            app_id=model.app_id,
            permission=model.permission,
        )

    @staticmethod
    def entity_to_model(entity: AppPermission) -> AppPermissionModel:
        return AppPermissionModel(
            app_id=entity.app_id,
            permission=entity.permission,
        )
