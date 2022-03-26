from prometheus_flask_exporter import Gauge, Counter

from api.database.db_session import create_session
from api.models.users import User

users_total = Gauge("users_total", "Total users count")
start_time = Gauge("start_time", "Start time")
apps_requests = Counter("apps_requests", "Requests by apps", ["id", "name", "path", "status"])


def update_users_count_metric():
    session = create_session()
    users_count = len(session.query(User).all())
    users_total.set(users_count)


def register_startup_metrics():
    start_time.set_to_current_time()
