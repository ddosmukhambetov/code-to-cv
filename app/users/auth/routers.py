from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends
from fastapi.responses import Response

from app.users.dependencies import get_current_user
from app.users.repos import UserRepo
from app.users.schemas import UserCreateSchema, UserReadSchema, AccessTokenSchema
from app.users.services import UserService

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED, summary='Register new user')
async def register(user_data: UserCreateSchema) -> UserReadSchema:
    return await UserService(UserRepo).register(user_data=user_data)


@router.post('/login', status_code=status.HTTP_200_OK, summary='Login user')
async def login(response: Response, username: str, password: str) -> AccessTokenSchema:
    return await UserService.login(response=response, username=username, password=password)


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT, summary='Logout user')
async def logout(response: Response, current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> None:
    return await UserService.logout(response=response)
