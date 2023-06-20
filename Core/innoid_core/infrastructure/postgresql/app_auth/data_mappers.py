from domain.app_auth.entities import AppApiKey
from .models import AppApiKeyModel


class AppApiKeyDataMapper:
    @staticmethod
    def model_to_entity(model: AppApiKeyModel) -> AppApiKey:
        return AppApiKey(
            app_id=model.app_id,
            created=model.created,
            hashed_value=model.hashed_value,
        )

    @staticmethod
    def entity_to_model(entity: AppApiKey) -> AppApiKeyModel:
        return AppApiKeyModel(
            app_id=entity.app_id,
            created=entity.created,
            hashed_value=entity.hashed_value,
        )
