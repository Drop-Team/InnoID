from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from api.models.users import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ("id",)
