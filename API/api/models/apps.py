from sqlalchemy import Column, Integer, String

from api.database.db_session import Base


class APIPermissions:
    get_user = 1  # get user by telegram_id
    manage_users = 2  # get all users, edit and remove user by telegram_id
    get_app = 3  # get app by id
    manage_apps = 4  # get all apps, edit and remove app by id


user_fields_numbers = {
    1: "is_authorized",
    2: "id",
    3: "telegram_id",
    4: "email"
}


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    token = Column(String, index=True, nullable=False)
    tg_author_id = Column(Integer, nullable=False)
    api_permissions = Column(Integer, default=1)
    allowed_user_fields = Column(Integer, default=1)
