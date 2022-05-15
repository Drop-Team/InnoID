from flask import Flask
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

import longpoll.logger
from longpoll.flask_config import Config
from longpoll.tools.metrics import register_startup_metrics

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app, path=None)


def create_app():
    """App creation"""
    app.config.from_object(Config)

    from longpoll.blueprints import events

    app.register_blueprint(events.blueprint)

    register_startup_metrics()

    return app
