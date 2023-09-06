from domain.modules.auth.jwt.entities import JWTRefreshToken
from .models import JWTRefreshTokenModel


class JWTRefreshTokenDataMapper:
    @staticmethod
    def model_to_entity(model: JWTRefreshTokenModel) -> JWTRefreshToken:
        return JWTRefreshToken(
            token_id=model.token_id,
            user_id=model.user_id,
            hashed_value=model.hashed_value,
            expires=model.expires,
        )

    @staticmethod
    def entity_to_model(entity: JWTRefreshToken) -> JWTRefreshTokenModel:
        return JWTRefreshTokenModel(
            token_id=entity.token_id,
            user_id=entity.user_id,
            hashed_value=entity.hashed_value,
            expires=entity.expires,
        )
