import asyncio
from pathlib import Path

from environs import Env

from src.users.repositories import UserRepository
from src.users.schemas import UserCreateSchema
from src.users.exceptions import UserAlreadyExistsException
from src.users.security import get_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = Env()
env.read_env(str(BASE_DIR / '.env'))

default_superuser_username: str = env.str('DEFAULT_SUPERUSER_USERNAME')
default_superuser_password: str = env.str('DEFAULT_SUPERUSER_PASSWORD')
default_is_active: bool = True
default_is_superuser: bool = True


async def create_superuser(data: UserCreateSchema) -> None:
    existing_user = await UserRepository.read_one_or_none(username=data.username)
    if existing_user:
        raise UserAlreadyExistsException
    data_dict = data.create_update_dict_superuser()
    data_dict['hashed_password'] = get_password_hash(data_dict.pop('password'))
    await UserRepository.create_one(**data_dict)

    formatted_output = f"""
    User Information:
    -----------------
    ID:              {data_dict.get('id')}
    Username:        {data_dict.get('username')}
    Hashed Password: {data_dict.get('hashed_password')}
    Is Active:       {data_dict.get('is_active')}
    Is Superuser:    {data_dict.get('is_superuser')}
    Created At:      {data_dict.get('created_at')}
    Updated At:      {data_dict.get('updated_at')}
    """
    print(formatted_output)


if __name__ == '__main__':
    asyncio.run(create_superuser(UserCreateSchema(
        username=default_superuser_username,
        password=default_superuser_password,
        is_active=default_is_active,
        is_superuser=default_is_superuser,
    )))
