import random
import uuid
from datetime import datetime

from .entities import UserCodeIdentification
from .errors import IdentificationNotFoundError
from .repositories import IUserCodeIdentificationRepository


class UserCodeIdentificationUseCase:
    user_code_identification_repository: IUserCodeIdentificationRepository

    def __init__(self, user_code_identification_repository: IUserCodeIdentificationRepository):
        self.user_code_identification_repository = user_code_identification_repository

    def get_by_code(self, code: int) -> UserCodeIdentification:
        user_code_identification = self.user_code_identification_repository.get_by_code(code)
        if not user_code_identification:
            raise IdentificationNotFoundError()
        # Remove since it's a one-time code
        self.user_code_identification_repository.remove(user_code_identification.identification_id)
        return user_code_identification

    def create(self, user_id: uuid.UUID) -> UserCodeIdentification:
        code = None
        while code is None or self.user_code_identification_repository.get_by_code(code):
            code = random.randint(100000, 999999)
        user_code_identification = UserCodeIdentification(
            identification_id=uuid.uuid4(),
            user_id=user_id,
            created=datetime.now(),
            code=code,
        )
        user_code_identification = self.user_code_identification_repository.add(user_code_identification)
        return user_code_identification

    def delete(self, user_code_identification_id: uuid.UUID) -> UserCodeIdentification:
        user_code_identification = self.user_code_identification_repository.remove(user_code_identification_id)
        if not user_code_identification:
            raise IdentificationNotFoundError()
        return user_code_identification
