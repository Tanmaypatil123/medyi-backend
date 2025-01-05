import uuid
from enum import Enum


class TokenGenerator:
    class GrantType(Enum):
        REFRESH_TOKEN = "refresh_token"
        FIREBASE = "firebase"
        PASSWORD = "password"

    @staticmethod
    def access_token():
        return str(uuid.uuid4()), 2 * 24 * 60 * 60

    @staticmethod
    def refresh_token():
        return str(uuid.uuid4()), 30 * 24 * 60 * 60
