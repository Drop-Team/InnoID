import uuid

from .entities import User
from .errors import UserNotFoundError
from .repositories import IUserRepository


class UserUseCase:
    user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_by_id(self, user_id: uuid.UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    def get_by_email(self, email: str) -> User:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    def get_list(self, offset: int = 0, limit: int = 100) -> list[User]:
        return self.user_repository.get_list(offset, limit)

    def create(self, email: str) -> User:
        user = User(
            user_id=self.user_repository.next_id(),
            email=email,
        )
        user = self.user_repository.add(user)
        return user
