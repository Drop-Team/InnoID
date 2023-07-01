from domain.user_auth.entities import UserRefreshToken
from .models import UserRefreshTokenModel


class UserRefreshTokenDataMapper:
    @staticmethod
    def model_to_entity(model: UserRefreshTokenModel) -> UserRefreshToken:
        return UserRefreshToken(
            token_id=model.token_id,
            user_id=model.user_id,
            hashed_value=model.hashed_value,
            expires=model.expires,
        )

    @staticmethod
    def entity_to_model(entity: UserRefreshToken) -> UserRefreshTokenModel:
        return UserRefreshTokenModel(
            token_id=entity.token_id,
            user_id=entity.user_id,
            hashed_value=entity.hashed_value,
            expires=entity.expires,
        )
