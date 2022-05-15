import os
import urllib

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cryptography.fernet import Fernet

from bot.tools.api_requests import ApiGet, ApiPut, ApiPost


def encrypt_telegram_id(telegram_id: str) -> str:
    encrypted = Fernet(os.getenv("INNOID_TELEGRAM_BOT_FERNET_KEY").encode()).encrypt(telegram_id.encode()).decode()
    encrypted_url_safe = urllib.parse.quote(encrypted)
    return encrypted_url_safe


def decrypt_telegram_id(encrypted_url_safe_telegram_id: str) -> str:
    encrypted = urllib.parse.unquote(encrypted_url_safe_telegram_id)
    decrypted = Fernet(os.getenv("INNOID_TELEGRAM_BOT_FERNET_KEY").encode()).decrypt(encrypted.encode())
    return decrypted.decode()


class User:
    id: int
    is_authorized: bool
    telegram_id: int
    email: str

    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id
        self.id = -1
        self.is_authorized = False
        self.email = ""
        self.update_data()

    def update_data(self):
        api_response = ApiGet.make_request("users", self.telegram_id)
        if api_response.status_code == 200:
            data = api_response.json()
            self.id = data["id"]
            self.is_authorized = data["is_authorized"]
            self.email = data["email"]

    def to_dict(self) -> dict:
        data = {
            "telegram_id": self.telegram_id,
            "is_authorized": self.is_authorized,
            "email": self.email
        }
        return data

    def save(self) -> bool:
        api_response = ApiPut.make_request("users", self.telegram_id, json=self.to_dict())
        if api_response.status_code == 200:
            return True
        if api_response.status_code == 404:
            api_response = ApiPost.make_request("users", json=self.to_dict())
            return api_response.status_code == 200
        return False

    def get_authorization_link(self):
        return "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize?" \
               "client_id={}&" \
               "response_type=code&" \
               "redirect_uri={}&" \
               "response_mode=query&" \
               "scope=User.ReadBasic.All" \
               "&state={}" \
            .format(os.getenv("INNOID_AZURE_CLIENT_ID"),
                    os.getenv("INNOID_REDIRECT_AFTER_LOGIN").replace("/", "%2F").replace(":", "%3A"),
                    encrypt_telegram_id(str(self.telegram_id))) \
            .replace(" ", "%20")

    def get_telegram_keyboard_markup(self) -> InlineKeyboardMarkup:
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton("Login", url=self.get_authorization_link()))
        return reply_markup


def get_user(telegram_id: int) -> User:
    user = User(telegram_id)
    return user
