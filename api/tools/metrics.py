from prometheus_flask_exporter import Gauge

from api.database.db_session import create_session
from api.models.users import User

users_total = Gauge("users_total", "Total users count")


def update_users_count_metric():
    session = create_session()
    users_count = len(session.query(User).all())
    users_total.set(users_count)
