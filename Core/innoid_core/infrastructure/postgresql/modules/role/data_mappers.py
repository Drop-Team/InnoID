from domain.modules.role.entities import UserRole, AppRole
from .models import UserRoleModel, AppRoleModel


class UserRoleDataMapper:
    @staticmethod
    def model_to_entity(model: UserRoleModel) -> UserRole:
        return UserRole(
            user_id=model.user_id,
            role=model.role,
        )

    @staticmethod
    def entity_to_model(entity: UserRole) -> UserRoleModel:
        return UserRoleModel(
            user_id=entity.user_id,
            role=entity.role,
        )


class AppRoleDataMapper:
    @staticmethod
    def model_to_entity(model: AppRoleModel) -> AppRole:
        return AppRole(
            app_id=model.app_id,
            role=model.role,
        )

    @staticmethod
    def entity_to_model(entity: AppRole) -> AppRoleModel:
        return AppRoleModel(
            app_id=entity.app_id,
            role=entity.role,
        )
