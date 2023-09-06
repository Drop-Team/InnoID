import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from domain.modules.auth.jwt.entities import JWTRefreshToken
from domain.modules.auth.jwt.repositories import IJWTRefreshTokenRepository
from .data_mappers import JWTRefreshTokenDataMapper
from .models import JWTRefreshTokenModel


class JWTRefreshTokenRepository(IJWTRefreshTokenRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, token_id: uuid.UUID) -> Optional[JWTRefreshToken]:
        user_refresh_token_model = self.session.query(JWTRefreshTokenModel).filter_by(token_id=token_id).one_or_none()
        if user_refresh_token_model:
            return JWTRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)
        return None

    def add(self, user_refresh_token: JWTRefreshToken) -> JWTRefreshToken:
        user_refresh_token_model = JWTRefreshTokenDataMapper.entity_to_model(user_refresh_token)
        self.session.add(user_refresh_token_model)
        self.session.commit()
        return JWTRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)

    def remove(self, token_id: uuid.UUID) -> Optional[JWTRefreshToken]:
        user_refresh_token_model = self.session.query(JWTRefreshTokenModel).filter_by(token_id=token_id).one_or_none()
        if not user_refresh_token_model:
            return None
        self.session.delete(user_refresh_token_model)
        self.session.commit()
        return JWTRefreshTokenDataMapper.model_to_entity(user_refresh_token_model)

    def next_id(self) -> uuid.UUID:
        return JWTRefreshToken.next_id()
