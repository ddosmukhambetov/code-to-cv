import uuid

from fastapi.responses import Response

from app.exceptions import AlreadyExistsException, NotFoundException
from app.users.auth.exceptions import IncorrectCredentialsException
from app.users.auth.security import get_password_hash, authenticate_user
from app.users.auth.tokens import create_access_token
from app.users.repos import UserRepo
from app.users.schemas import UserCreateSchema, UserReadSchema, AccessTokenSchema, UserUpdateSchema, \
    AdminUserUpdateSchema


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def register(self, user_data: UserCreateSchema) -> UserReadSchema:
        existing_user = await self.user_repo.check_existing_user(username=user_data.username, email=user_data.email)
        if existing_user:
            if existing_user.username == user_data.username:
                raise AlreadyExistsException('Username')
            if existing_user.email == user_data.email:
                raise AlreadyExistsException('Email')
        user_data.password = get_password_hash(user_data.password)
        user = await self.user_repo.create_one(**user_data.model_dump())
        return user

    @staticmethod
    async def login(response: Response, username: str, password: str) -> AccessTokenSchema:
        user = await authenticate_user(username=username, password=password)
        if not user:
            raise IncorrectCredentialsException
        access_token = await create_access_token(user=user)
        response.set_cookie(key='access-token', value=access_token, httponly=True)
        return AccessTokenSchema(access_token=access_token)

    @staticmethod
    async def logout(response: Response) -> None:
        response.delete_cookie(key='access-token')

    async def update_me(self, response: Response, user_data: UserUpdateSchema, user_uuid: uuid.UUID) -> UserReadSchema:
        if user_data.username or user_data.email:
            existing_user = await self.user_repo.check_existing_user(username=user_data.username, email=user_data.email)
            if existing_user:
                if existing_user.username == user_data.username:
                    raise AlreadyExistsException('Username')
                if existing_user.email == user_data.email:
                    raise AlreadyExistsException('Email')
        if user_data.password:
            user_data.password = get_password_hash(user_data.password)
        user = await self.user_repo.update_by_uuid(object_uuid=user_uuid, **user_data.model_dump(exclude_unset=True))
        response.set_cookie(key='access-token', value=await create_access_token(user=user), httponly=True)
        return user

    async def delete_me(self, response: Response, user_uuid: uuid.UUID) -> None:
        await self.user_repo.delete_by_uuid(object_uuid=user_uuid)
        response.delete_cookie(key='access-token')

    async def get_user_by_username(self, username: str):
        user = await self.user_repo.get_one_or_none_without_active_true(username=username)
        if not user:
            raise NotFoundException('User')
        return user

    async def update_user_by_username(self, username: str, user_data: AdminUserUpdateSchema) -> UserReadSchema:
        user = await self.user_repo.get_one_or_none_without_active_true(username=username)
        if not user:
            raise NotFoundException('User')
        user = await self.user_repo.update_by_uuid(object_uuid=user.uuid, **user_data.model_dump(exclude_unset=True))
        return user

    async def delete_user_by_username(self, username: str) -> None:
        user = await self.user_repo.get_one_or_none_without_active_true(username=username)
        if not user:
            raise NotFoundException('User')
        await self.user_repo.delete_by_uuid(object_uuid=user.uuid)
