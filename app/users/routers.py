from typing import Annotated

from fastapi import APIRouter, status
from fastapi import Depends
from fastapi.responses import Response

from app.users.dependencies import get_current_user, get_current_superuser
from app.users.repos import UserRepo
from app.users.schemas import UserReadSchema, UserUpdateSchema, AdminUserUpdateSchema
from app.users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', status_code=status.HTTP_200_OK, summary='Get current user')
async def get_me(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> UserReadSchema:
    return current_user


@router.patch('/me', status_code=status.HTTP_200_OK, summary='Update current user')
async def update_me(
        response: Response,
        user_data: UserUpdateSchema,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> UserReadSchema:
    return await UserService(UserRepo).update_me(response=response, user_data=user_data, user_uuid=current_user.uuid)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT, summary='Delete current user')
async def delete_me(response: Response, current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> None:
    return await UserService(UserRepo).delete_me(response=response, user_uuid=current_user.uuid)


@router.get('/{username}', status_code=status.HTTP_200_OK, summary='Get user by username')
async def get_user_by_username(
        username: str,
        current_superuser: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> UserReadSchema:
    return await UserService(UserRepo).get_user_by_username(username=username)


@router.patch('/{username}', status_code=status.HTTP_200_OK, summary='Update user by username')
async def update_user_by_username(
        username: str,
        user_data: AdminUserUpdateSchema,
        current_superuser: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> UserReadSchema:
    return await UserService(UserRepo).update_user_by_username(username=username, user_data=user_data)


@router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete user by username')
async def delete_user_by_username(
        username: str,
        current_superuser: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> None:
    return await UserService(UserRepo).delete_user_by_username(username=username)
