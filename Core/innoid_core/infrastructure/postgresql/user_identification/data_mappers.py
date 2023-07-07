from domain.user_identification.entities import UserCodeIdentification
from .models import UserCodeIdentificationModel


class UserCodeIdentificationDataMapper:
    @staticmethod
    def model_to_entity(model: UserCodeIdentificationModel) -> UserCodeIdentification:
        return UserCodeIdentification(
            identification_id=model.identification_id,
            user_id=model.user_id,
            created=model.created,
            code=model.code,
        )

    @staticmethod
    def entity_to_model(entity: UserCodeIdentification) -> UserCodeIdentificationModel:
        return UserCodeIdentificationModel(
            identification_id=entity.identification_id,
            user_id=entity.user_id,
            created=entity.created,
            code=entity.code,
        )
