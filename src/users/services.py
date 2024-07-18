from fastapi import Response

from src.users.exceptions import (UserAlreadyExistsException, IncorrectCredentialsException,
                                  UserNotPresentException)
from src.users.repositories import UserRepository
from src.users.schemas import UserCreateSchema, UserReadSchema, AccessTokenSchema, UserUpdateSchema
from src.users.security import authenticate_user, create_access_token, get_password_hash
from src.users.utils import prepare_and_update_user


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    async def user_register(self, data: UserCreateSchema) -> UserReadSchema:
        existing_user = await self.user_repository.read_one_or_none(username=data.username)
        if existing_user:
            raise UserAlreadyExistsException
        data_dict = data.create_update_dict()
        data_dict['hashed_password'] = get_password_hash(data_dict.pop('password'))
        result = await self.user_repository.create_one(**data_dict)
        return result

    @staticmethod
    async def user_login(username: str, password: str, response: Response) -> AccessTokenSchema:
        user = await authenticate_user(username, password)
        if not user:
            raise IncorrectCredentialsException
        access_token = create_access_token(data={'sub': str(username)})
        response.set_cookie(key='code-to-cv-token', value=access_token, httponly=True)
        return AccessTokenSchema(access_token=access_token, token_type='bearer')

    @staticmethod
    async def user_logout(response: Response) -> None:
        response.delete_cookie('code-to-cv-token')

    async def user_update_me(
            self,
            user_data: UserUpdateSchema,
            current_user_id: int,
            response: Response,
    ) -> UserReadSchema:
        return await prepare_and_update_user(
            user_id=current_user_id,
            create_update_dict_func=user_data.create_update_dict,
            user_repository=self.user_repository,
            if_self_update=True,
            response=response,
        )

    async def user_delete_me(self, current_user_id: int) -> None:
        user = await self.user_repository.read_by_id_or_none(current_user_id)
        if not user:
            raise UserNotPresentException
        await self.user_repository.delete_by_id(current_user_id)

    async def admin_get_user(self, user_id: int):
        user = await self.user_repository.read_by_id_or_none(user_id)
        if not user:
            raise UserNotPresentException
        return user

    async def admin_update_user(
            self,
            user_id: int,
            user_data: UserUpdateSchema,
            admin_user_id: int,
            response: Response,
    ) -> UserReadSchema:
        if_self_update = (admin_user_id == user_id)
        return await prepare_and_update_user(
            user_id=user_id,
            create_update_dict_func=user_data.create_update_dict,
            user_repository=self.user_repository,
            if_self_update=if_self_update,
            response=response,
        )

    async def admin_delete_user(self, user_id: int) -> None:
        user = await self.user_repository.read_by_id_or_none(user_id)
        if not user:
            raise UserNotPresentException
        await self.user_repository.delete_by_id(user_id)
