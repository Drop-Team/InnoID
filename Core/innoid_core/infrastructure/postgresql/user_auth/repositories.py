import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.user_auth.entities import UserRefreshToken
from domain.user_auth.repositories import IUserRefreshTokenRepository
from .data_mappers import UserRefreshTokenDataMapper
from .models import UserRefreshTokenModel


class UserRefreshTokenRepository(IUserRefreshTokenRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, token_id: uuid.UUID) -> Optional[UserRefreshToken]:
        user_refresh_token_model = self.session.query(UserRefreshTokenModel).filter_by(token_id=token_id).one_or_none()
        if user_refresh_token_model:
            return UserRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)
        return None

    def add(self, user_refresh_token: UserRefreshToken) -> UserRefreshToken:
        user_refresh_token_model = UserRefreshTokenDataMapper.entity_to_model(user_refresh_token)
        self.session.add(user_refresh_token_model)
        self.session.commit()
        return UserRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)

    def remove(self, token_id: uuid.UUID) -> Optional[UserRefreshToken]:
        user_refresh_token_model = self.session.query(UserRefreshTokenModel).filter_by(token_id=token_id).one_or_none()
        if not user_refresh_token_model:
            return None
        self.session.delete(user_refresh_token_model)
        self.session.commit()
        return UserRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)

    def next_id(self) -> uuid.UUID:
        return UserRefreshToken.next_id()
