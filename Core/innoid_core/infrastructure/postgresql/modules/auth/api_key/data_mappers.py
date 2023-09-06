from domain.modules.auth.api_key.entities import ApiKey
from .models import ApiKeyModel


class ApiKeyDataMapper:
    @staticmethod
    def model_to_entity(model: ApiKeyModel) -> ApiKey:
        return ApiKey(
            app_id=model.app_id,
            created=model.created,
            hashed_value=model.hashed_value,
        )

    @staticmethod
    def entity_to_model(entity: ApiKey) -> ApiKeyModel:
        return ApiKeyModel(
            app_id=entity.app_id,
            created=entity.created,
            hashed_value=entity.hashed_value,
        )
