from typing import Callable, Optional

from fastapi import Response

from src.users.exceptions import UserAlreadyExistsException, IncorrectCredentialsException
from src.users.repositories import UserRepository
from src.users.schemas import UserReadSchema
from src.users.security import get_password_hash, create_access_token


async def prepare_and_update_user(
        user_id: int,
        create_update_dict_func: Callable[[], dict],
        user_repository: UserRepository,
        if_self_update: bool = False,
        response: Optional[Response] = None,
) -> UserReadSchema:
    user = await user_repository.read_by_id_or_none(user_id)
    if not user:
        raise IncorrectCredentialsException

    data_dict = create_update_dict_func()

    if data_dict.get('username'):
        existing_user = await user_repository.read_one_or_none(username=data_dict.get('username'))
        if existing_user:
            raise UserAlreadyExistsException

    if data_dict.get('password'):
        data_dict['hashed_password'] = get_password_hash(data_dict.pop('password'))
    updated_user = await user_repository.update_by_id(user_id, **data_dict)

    if if_self_update and response and ('username' in data_dict or 'hashed_password' in data_dict):
        access_token = create_access_token(data={'sub': str(updated_user.get('username'))})
        response.set_cookie(key='code-to-cv-token', value=access_token, httponly=True)

    return updated_user
