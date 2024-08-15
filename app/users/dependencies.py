from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from app.exceptions import NotFoundException
from app.users.auth.tokens import decode_json_web_token
from app.users.exceptions import PermissionDeniedException, UnauthorizedException
from app.users.repos import UserRepo
from app.users.schemas import UserReadSchema


async def get_token(request: Request) -> str:
    if token := request.cookies.get('access-token'):
        return token
    raise UnauthorizedException


async def get_current_user(token: Annotated[str, Depends(get_token)]) -> UserReadSchema:
    data = await decode_json_web_token(token=token)
    username = data.get('username')
    if user := await UserRepo.get_one_or_none(username=username):
        return user
    raise NotFoundException('User')


async def get_current_superuser(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> UserReadSchema:
    if current_user.is_superuser:
        return current_user
    raise PermissionDeniedException
