#!/usr/bin/env python
import os

from dotenv import load_dotenv
from prometheus_client import start_http_server


def main():
    load_dotenv("../.env")
    import bot
    start_http_server(int(os.getenv("INNOID_TELEGRAM_BOT_PROMETHEUS_PORT")))
    bot.start()


if __name__ == '__main__':
    main()
