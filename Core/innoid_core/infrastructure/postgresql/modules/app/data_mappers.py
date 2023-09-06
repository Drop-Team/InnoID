from domain.modules.app.entities import App
from .models import AppModel


class AppDataMapper:
    @staticmethod
    def model_to_entity(model: AppModel) -> App:
        return App(
            app_id=model.app_id,
            name=model.name,
            owner_id=model.owner_id,
        )

    @staticmethod
    def entity_to_model(entity: App) -> AppModel:
        return AppModel(
            app_id=entity.app_id,
            name=entity.name,
            owner_id=entity.owner_id,
        )
