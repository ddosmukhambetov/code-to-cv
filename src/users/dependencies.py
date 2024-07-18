from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Request, Depends
from jwt import InvalidTokenError

from src.config import settings
from src.users.exceptions import NotAuthorizedException, TokenExpiredException, TokenInvalidException, PermissionDenied
from src.users.repositories import UserRepository
from src.users.schemas import UserReadSchema


def get_token(request: Request):
    token = request.cookies.get('code-to-cv-token')
    if not token:
        raise NotAuthorizedException
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    try:
        payload = jwt.decode(token, settings.app.jwt_secret_key, algorithms=[settings.app.jwt_algorithm])
        username: str = payload.get('sub')
        expire = payload.get('exp')
        if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
            raise TokenExpiredException
        if not username:
            raise NotAuthorizedException
    except InvalidTokenError:
        raise TokenInvalidException
    user = await UserRepository.read_one_or_none(username=username)
    if not user:
        raise NotAuthorizedException
    return user


async def get_current_superuser(current_user: Annotated[UserReadSchema, Depends(get_current_user)]):
    if not current_user.is_superuser:
        raise PermissionDenied
    return current_user
