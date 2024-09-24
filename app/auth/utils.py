import uuid
from datetime import timedelta, datetime
import jwt
from passlib.context import CryptContext
import logging
from app import auth_settings

passwd_context = CryptContext(
    schemes=["bcrypt"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 3600


def generate_passwd_hash(password: str) -> str:
    password_hash = passwd_context.hash(password)
    return password_hash


def verify_passwd_hash(password: str, hashed_password: str) -> bool:
    password_hash = passwd_context.verify(password, hashed_password)
    return password_hash


def create_access_token(data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {"user": data, 'exp': datetime.now() + expiry if expiry else timedelta(
        seconds=auth_settings.access_token_expire_seconds), "jti": str(uuid.uuid4()),
               "refresh_token": refresh}
    token = jwt.encode(
        payload=payload,
        key=auth_settings.SECRET_KEY,
        algorithm=auth_settings.ALGORITHM,
    )
    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=auth_settings.SECRET_KEY,
            algorithms=[auth_settings.ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
