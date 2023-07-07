import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.user_identification.entities import UserCodeIdentification
from domain.user_identification.repositories import IUserCodeIdentificationRepository
from .data_mappers import UserCodeIdentificationDataMapper
from .models import UserCodeIdentificationModel


class UserCodeIdentificationRepository(IUserCodeIdentificationRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: int) -> Optional[UserCodeIdentification]:
        user_code_identification_model = self.session.query(UserCodeIdentificationModel).filter_by(
            code=code).one_or_none()
        if user_code_identification_model:
            return UserCodeIdentificationDataMapper.model_to_entity(user_code_identification_model)
        return None

    def add(self, user_code_identification: UserCodeIdentification) -> UserCodeIdentification:
        user_code_identification_model = UserCodeIdentificationDataMapper.entity_to_model(user_code_identification)
        self.session.add(user_code_identification_model)
        self.session.commit()
        return UserCodeIdentificationDataMapper.model_to_entity(user_code_identification_model)

    def remove(self, identification_id: uuid.UUID) -> Optional[UserCodeIdentification]:
        user_code_identification_model = self.session.query(UserCodeIdentificationModel).filter_by(
            identification_id=identification_id).one_or_none()
        if not user_code_identification_model:
            return None
        self.session.delete(user_code_identification_model)
        self.session.commit()
        return UserCodeIdentificationDataMapper.model_to_entity(user_code_identification_model)
