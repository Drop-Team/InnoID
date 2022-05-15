from prometheus_flask_exporter import Gauge

start_time = Gauge("start_time", "Start time")


def register_startup_metrics():
    start_time.set_to_current_time()
