from fastapi import FastAPI

from api.v2 import fastapi_app as fastapi_app_v2
from infrastructure.postgresql.database import setup_database

setup_database()

app = FastAPI()

app.mount("/v2", fastapi_app_v2.get_app())
