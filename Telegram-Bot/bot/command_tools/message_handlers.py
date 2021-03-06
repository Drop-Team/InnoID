from bot.logger import logger
from bot.metrics import Metrics


def get_new_function(old_function):
    def new_function(msg):
        log_msg = f"{msg.from_user.mention} ({msg.from_user.id}) "
        if msg.text and msg.text.startswith("/"):
            log_msg += f"used command '{msg.text}'"

            command_name = msg.text.split()[0].split("/")[1]
            Metrics.message_handler_commands.labels(command_name).inc()
        else:
            log_msg += "sent message"
        log_msg += f", raised function '{old_function.__name__}'"
        logger.info(log_msg)

        Metrics.messages.inc()
        Metrics.message_handler_functions.labels(f"{old_function.__name__}").inc()
        return old_function(msg)

    return new_function


class MessageHandler:
    def __init__(self, func, custom_filters, commands, content_types, equals, blacklist, is_not_command):
        self.func = get_new_function(func)
        self.custom_filters = list(custom_filters)
        self.commands = commands
        self.content_types = ["any"] if content_types is None else content_types
        if equals is not None:
            self.custom_filters.append(lambda msg: msg.text == equals)
        if blacklist is not None:
            self.custom_filters.append(lambda msg: msg.text not in blacklist)
        if is_not_command == True:
            self.custom_filters.append(lambda msg: not msg.text.startswith("/"))


def add_message_handler(*custom_filters, commands=None, content_types=None, equals=None,
                        blacklist=None, is_not_command=None):
    """decorator for message handlers"""

    def decorator(handler_func):
        message_handlers.append(MessageHandler(handler_func, custom_filters, commands, content_types, equals,
                                               blacklist, is_not_command))
        return handler_func

    return decorator


def register_message_handlers(dp):
    """register all message handlers in dispatcher"""
    for handler in message_handlers:
        dp.register_message_handler(handler.func,
                                    *handler.custom_filters,
                                    commands=handler.commands,
                                    content_types=handler.content_types)


message_handlers = []
