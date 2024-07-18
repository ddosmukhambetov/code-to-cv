from datetime import timedelta, datetime, timezone

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.users.repositories import UserRepository

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=45)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.app.jwt_secret_key, algorithm=settings.app.jwt_algorithm)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UserRepository.read_one_or_none(username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
