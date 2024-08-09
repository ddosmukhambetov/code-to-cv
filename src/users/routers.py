from typing import Annotated

from fastapi import APIRouter, Response, Depends, status

from src.users.dependencies import get_current_user, get_current_superuser
from src.users.repositories import UserRepository
from src.users.schemas import UserCreateSchema, UserReadSchema, AccessTokenSchema, UserUpdateSchema
from src.users.services import UserService

auth_router = APIRouter(prefix='/auth', tags=['Auth'])
users_router = APIRouter(prefix='/users', tags=['Users'])


# ! Auth
@auth_router.post('/register', summary='Register a new user account', status_code=status.HTTP_201_CREATED)
async def user_register(data: UserCreateSchema) -> UserReadSchema:
    return await UserService(UserRepository).user_register(data)


@auth_router.post('/login', summary='Authenticate and obtain an access token', status_code=status.HTTP_200_OK)
async def user_login(username: str, password: str, response: Response) -> AccessTokenSchema:
    return await UserService(UserRepository).user_login(username, password, response)


@auth_router.post('/logout', summary='Log out from the current session', status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(current_user: Annotated[UserReadSchema, Depends(get_current_user)], response: Response) -> None:
    await UserService(UserRepository).user_logout(response)


# ! Users
@users_router.get('/me', summary='Retrieve the current user profile information', status_code=status.HTTP_200_OK)
async def user_me(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> UserReadSchema:
    return current_user


@users_router.patch('/me', summary='Update the current user profile information', status_code=status.HTTP_200_OK)
async def user_update_me(
        user_data: UserUpdateSchema,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
        response: Response,
) -> UserReadSchema:
    return await UserService(UserRepository).user_update_me(user_data, current_user.id, response)


@users_router.delete('/me', summary='Delete the current user profile', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_me(
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
        response: Response,
) -> None:
    return await UserService(UserRepository).user_delete_me(current_user.id, response)


# Admin Router
@users_router.get('/{user_id}', summary='Retrieve a user profile by ID', status_code=status.HTTP_200_OK)
async def admin_get_user(
        user_id: int,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> UserReadSchema:
    return await UserService(UserRepository).admin_get_user(user_id)


@users_router.patch('/{user_id}', summary='Update a user profile by ID', status_code=status.HTTP_200_OK)
async def admin_update_user(
        user_id: int,
        user_data: UserUpdateSchema,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
        response: Response,
) -> UserReadSchema:
    return await UserService(UserRepository).admin_update_user(user_id, user_data, admin_user.id, response)


@users_router.delete('/{user_id}', summary='Delete a user profile by ID', status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
        user_id: int,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> None:
    return await UserService(UserRepository).admin_delete_user(user_id)
