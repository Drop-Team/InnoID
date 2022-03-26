import secrets

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from marshmallow.exceptions import ValidationError

from api.database.db_session import create_session
from api.models.apps import App, APIPermissions
from api.schemas.apps import AppSchema
from api.tools import errors
from api.tools.metrics import update_apps_count_metric
from api.tools.requests import auth_check
from api.tools.response import success_message

blueprint = Blueprint(
    "apps_resource",
    __name__,
)
api = Api(blueprint)


class AppResource(Resource):
    @auth_check(APIPermissions.get_app)
    def get(self, app_id: int, user_fields: list[int]):
        session = create_session()
        app = session.query(App).filter(App.id == app_id).first()
        if not app:
            raise errors.AppNotFoundError
        return AppSchema().dump(app)

    @auth_check(APIPermissions.manage_apps)
    def put(self, app_id: int, user_fields: list[int]):
        data = request.get_json()
        if not data:
            raise errors.InvalidRequestError()

        try:
            AppSchema(partial=True).load(data)
        except ValidationError as e:
            raise errors.InvalidRequestError(e.messages)

        session = create_session()
        app = session.query(App).filter(App.id == app_id).first()
        if not app:
            raise errors.AppNotFoundError

        session.query(App).filter(App.id == app_id).update(data)
        session.commit()

        return success_message({"app": AppSchema().dump(app)})

    @auth_check(APIPermissions.manage_apps)
    def delete(self, app_id: int, user_fields: list[int]):
        session = create_session()
        app = session.query(App).filter(App.id == app_id).first()
        if not app:
            raise errors.AppNotFoundError

        session.delete(app)
        session.commit()

        update_apps_count_metric()

        return success_message({"app": AppSchema().dump(app)})


class AppsListResource(Resource):
    @auth_check(APIPermissions.manage_apps)
    def get(self, user_fields: list[int]):
        session = create_session()
        apps = session.query(App).all()
        return jsonify({
            "apps": AppSchema(exclude=("token",)).dump(apps, many=True)
        })

    @auth_check(APIPermissions.manage_apps)
    def post(self, user_fields: list[int]):
        data = request.get_json()
        try:
            AppSchema().load(data)
        except ValidationError as e:
            raise errors.InvalidRequestError(e.messages)

        session = create_session()

        app_token = secrets.token_hex(16)
        while session.query(App).filter(App.token == app_token).first() is not None:
            app_token = secrets.token_hex(16)

        app = App(**data)
        app.token = app_token
        app.api_permissions = 1
        app.allowed_user_fields = 1

        session.add(app)
        session.commit()

        update_apps_count_metric()

        return success_message({"app": AppSchema().dump(app)})


class AppResetToken(Resource):
    @auth_check(APIPermissions.manage_apps)
    def put(self, app_id: int, user_fields: list[int]):
        session = create_session()
        app = session.query(App).filter(App.id == app_id).first()
        if not app:
            raise errors.AppNotFoundError

        app_token = secrets.token_hex(16)
        while session.query(App).filter(App.token == app_token).first() is not None:
            app_token = secrets.token_hex(16)

        app.token = app_token
        session.commit()

        return success_message({"app": AppSchema().dump(app)})


api.add_resource(AppResource, "/apps/<int:app_id>")
api.add_resource(AppsListResource, "/apps")
api.add_resource(AppResetToken, "/apps/<int:app_id>/reset_token")
