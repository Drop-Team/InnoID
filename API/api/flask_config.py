import os


class Config:
    SECRET_KEY = os.getenv("INNOID_API_FLASK_SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True
