import os


class Config:
    SERVE_PORT = os.getenv(
        "SERVE_PORT", "22512"
    )
    POSTGRES_CONNECTION_STRING = os.getenv(
        "POSTGRES_CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/innoid_core"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "..."
    )

    MS_AD_CLIENT_ID = os.getenv(
        "MS_AD_CLIENT_ID", "..."
    )
    MS_AD_CLIENT_SECRET = os.getenv(
        "MS_AD_CLIENT_SECRET", "..."
    )
    MS_AD_DOMAIN_HINT = os.getenv(
        "MS_AD_DOMAIN_HINT", "innopolis.ru"
    )
    MS_AD_REDIRECT_URI = os.getenv(
        "MS_AD_REDIRECT_URI", "https://innoid.dropteam.ru/login"
    )
