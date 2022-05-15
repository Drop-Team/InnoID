from prometheus_client import Counter, Gauge


class Metrics:
    start_time = Gauge("start_time", "Start time")

    messages = Counter("messages", "Total messages received")
    message_handler_functions = Counter("message_handler_functions", "Raised functions", ["name"])
    message_handler_commands = Counter("message_handler_commands", "Command names", ["name"])

    callback_queries = Counter("callback_queries", "Total callback queries processed")
    callback_queries_functions = Counter("callback_queries_functions", "Raised functions", ["name"])

    logs = Counter("logs", "log records", ["name", "level"])

    event_check = Counter("event_check", "Has an event check been performed", ["status"])
    event_check.labels("success")
    event_check.labels("fail")
