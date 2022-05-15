import os

from api.database.db_session import create_session
from api.models.apps import App, APIPermissions, user_fields_numbers
from api.tools.requests import encode_numbers


def check_default_app():
    session = create_session()
    app_token = os.getenv("INNOID_API_SERVICE_APP_TOKEN")
    api_permissions = encode_numbers([
        APIPermissions.get_user,
        APIPermissions.manage_users,
        APIPermissions.get_app,
        APIPermissions.manage_apps
    ])
    user_fields = encode_numbers(user_fields_numbers.keys())

    app = session.query(App).filter(App.id == 1).first()
    if not app:
        app = App()
        app.tg_author_id = 0
        app.name = "ServiceApp"
        app.token = app_token
        app.api_permissions = api_permissions
        app.allowed_user_fields = user_fields
        session.add(app)
    else:
        app.token = app_token
        app.api_permissions = api_permissions
        app.allowed_user_fields = user_fields

    session.commit()
