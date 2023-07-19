import os


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN", "5066660695:AAESipsZkE0xdajZLlOz985-rDKciGhb4Nc"
    )
    API_URL = os.getenv("API_URL", "http://localhost:8000")
