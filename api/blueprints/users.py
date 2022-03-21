from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from marshmallow.exceptions import ValidationError

from api.database.db_session import create_session
from api.models.apps import APIPermissions, user_fields_numbers
from api.models.users import User
from api.schemas.users import UserSchema
from api.tools import errors
from api.tools.metrics import update_users_count_metric
from api.tools.requests import auth_check
from api.tools.response import success_message

blueprint = Blueprint(
    "users_resource",
    __name__,
)
api = Api(blueprint)


def get_user_json_data(user: User, user_fields: list[int]):
    user_original_data = user.__dict__
    new_data = dict()

    for user_field in user_fields:
        field_name = user_fields_numbers[user_field]
        if field_name in user_original_data:
            new_data[field_name] = user_original_data[field_name]

    return new_data


class UserResource(Resource):
    @auth_check(APIPermissions.get_user)
    def get(self, telegram_id: int, user_fields: list[int]):
        session = create_session()
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise errors.UserNotFoundError
        return get_user_json_data(user, user_fields)

    @auth_check(APIPermissions.manage_users)
    def put(self, telegram_id: int, user_fields: list[int]):
        data = request.get_json()
        if not data:
            raise errors.InvalidRequestError()

        try:
            UserSchema(partial=True).load(data)
        except ValidationError as e:
            raise errors.InvalidRequestError(e.messages)

        session = create_session()
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise errors.UserNotFoundError

        session.query(User).filter(User.telegram_id == telegram_id).update(data)
        session.commit()

        return success_message({"user": UserSchema().dump(user)})


class UsersListResource(Resource):
    @auth_check(APIPermissions.manage_users)
    def get(self, user_fields: list[int]):
        session = create_session()
        users = session.query(User).all()
        return jsonify({
            "users": UserSchema().dump(users, many=True)
        })

    @auth_check(APIPermissions.manage_users)
    def post(self, user_fields: list[int]):
        data = request.get_json()
        try:
            UserSchema().load(data)
        except ValidationError as e:
            raise errors.InvalidRequestError(e.messages)

        session = create_session()

        existing_user = session.query(User).filter(
            (User.telegram_id == data["telegram_id"]) | (User.email == data["email"])).first()
        if existing_user is not None:
            raise errors.UserAlreadyExistsError

        user = User(**data)
        session.add(user)
        session.commit()

        update_users_count_metric()

        return success_message({"user": UserSchema().dump(user)})


api.add_resource(UserResource, "/users/<int:telegram_id>")
api.add_resource(UsersListResource, "/users")
