from prometheus_flask_exporter import Gauge, Counter

from api.database.db_session import create_session
from api.models.apps import App
from api.models.users import User

from datetime import datetime

users_total = Gauge("users_total", "Total users count", ["update_time"])
apps_total = Gauge("apps_total", "Total apps count", ["update_time"])
start_time = Gauge("start_time", "Start time")
apps_requests = Counter("apps_requests", "Requests by apps", ["id", "name", "path", "status"])


def update_users_count_metric():
    session = create_session()
    users_count = len(session.query(User).all())
    users_total.labels(datetime.now().timestamp()).set(users_count)


def update_apps_count_metric():
    session = create_session()
    apps_count = len(session.query(App).all())
    apps_total.labels(datetime.now().timestamp()).set(apps_count)


def register_startup_metrics():
    start_time.set_to_current_time()
