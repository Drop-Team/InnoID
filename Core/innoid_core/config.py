import os


class Config:
    SERVE_PORT = os.getenv(
        "SERVE_PORT", "22512"
    )
    POSTGRES_CONNECTION_STRING = os.getenv(
        "POSTGRES_CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/innoid_core"
    )
