import uuid
from datetime import timedelta, datetime, timezone

import jwt

from app.core.config import settings
from app.users.auth.exceptions import TokenExpiredException, InvalidTokenException
from app.users.schemas import UserReadSchema

token_type_field = 'type'
access_token_type = 'access'


async def create_json_web_token(
        token_type: str,
        data: dict,
        expire_minutes: int = settings.auth.access_token_expire_minutes,
        expires_delta: timedelta | None = None,
        secret_key: str = settings.auth.token_secret_key,
        algorithm: str = settings.auth.algorithm,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, type=token_type, iat=datetime.now(timezone.utc), jti=str(uuid.uuid4()))
    encoded_jwt = jwt.encode(to_encode, key=secret_key, algorithm=algorithm)
    return encoded_jwt


async def create_access_token(user: UserReadSchema) -> str:
    data = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
    }
    return await create_json_web_token(
        token_type=access_token_type,
        data=data,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


async def decode_json_web_token(token: str) -> dict:
    try:
        data = jwt.decode(token, key=settings.auth.token_secret_key, algorithms=[settings.auth.algorithm])
        username, expire = data.get('sub'), data.get('exp')
        if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
            raise TokenExpiredException
        if not username:
            raise InvalidTokenException
    except jwt.PyJWTError:
        raise InvalidTokenException
    return data
