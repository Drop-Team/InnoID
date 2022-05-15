import multiprocessing
import os

from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

bind = "0.0.0.0:{}".format(os.getenv("INNOID_API_FLASK_PORT"))
workers = multiprocessing.cpu_count() * 2 + 1


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(int(os.getenv("INNOID_API_METRICS_PORT")))


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


def on_starting(server):
    for fn in os.listdir(os.getenv("PROMETHEUS_MULTIPROC_DIR")):
        if fn == ".keep":
            continue

        os.remove(os.getenv("PROMETHEUS_MULTIPROC_DIR") + "/" + fn)
