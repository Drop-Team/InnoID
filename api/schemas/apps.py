from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from api.models.apps import App


class AppSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = App
        dump_only = ("id", "token",)
