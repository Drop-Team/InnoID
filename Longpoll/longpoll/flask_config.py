import os


class Config:
    SECRET_KEY = os.getenv("INNOID_LONGPOLL_FLASK_SECRET_KEY")
