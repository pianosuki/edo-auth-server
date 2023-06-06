import secrets, uuid
from app import bcrypt


def generate_uuid() -> str:
    return uuid.uuid4().hex


def generate_token(length: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
