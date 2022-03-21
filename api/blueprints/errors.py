from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from api.tools.errors import ApiError, DatabaseError

blueprint = Blueprint(
    "api_errors",
    __name__,
)


@blueprint.app_errorhandler(ApiError)
def app_errors_handler(error):
    return error.create_response()


@blueprint.app_errorhandler(IntegrityError)
def database_errors_handler(error):
    return DatabaseError().create_response()
