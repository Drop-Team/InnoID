# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

import api.logger
from api.database import db_session
from api.flask_config import Config
from api.tools.default_app import check_default_app
from api.tools.metrics import update_users_count_metric, update_apps_count_metric, register_startup_metrics

app = Flask(__name__)
cors = CORS(app)
metrics = GunicornPrometheusMetrics(app, path=None)


def create_app():
    """App creation"""
    app.config.from_object(Config)

    from api.blueprints import apps, users
    from api.blueprints import errors as api_errors

    api_url_prefix = "/v1"
    app.register_blueprint(api_errors.blueprint)
    app.register_blueprint(apps.blueprint, url_prefix=api_url_prefix)
    app.register_blueprint(users.blueprint, url_prefix=api_url_prefix)

    db_session.database_init("app.db")
    check_default_app()

    register_startup_metrics()
    update_users_count_metric()
    update_apps_count_metric()

    return app
