import logging

from prometheus_flask_exporter import Counter

logs_metrics = Counter("logs", "log records", ["name", "level"])


class LogsHandler(logging.Handler):
    def emit(self, record):
        logs_metrics.labels(record.name, record.levelname).inc()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
    filename="app.log"
)

logger = logging.getLogger("app")

gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger.addHandler(LogsHandler())

logging.getLogger().addHandler(LogsHandler())
