from domain.modules.user.entities import User
from .models import UserModel


class UserDataMapper:
    @staticmethod
    def model_to_entity(model: UserModel) -> User:
        return User(
            user_id=model.user_id,
            email=model.email,
        )

    @staticmethod
    def entity_to_model(entity: User) -> UserModel:
        return UserModel(
            user_id=entity.user_id,
            email=entity.email,
        )
