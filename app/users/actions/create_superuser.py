import asyncio
import sys
from pathlib import Path

from environs import Env
from pydantic import EmailStr

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from app.exceptions import AlreadyExistsException
from app.users.auth.security import get_password_hash
from app.users.repos import UserRepo

env = Env()
env.read_env(str(BASE_DIR / '.env'))

default_superuser_username: str = env.str('DEFAULT_SUPERUSER_USERNAME')
default_superuser_email: EmailStr = env.str('DEFAULT_SUPERUSER_EMAIL')
default_superuser_password: str = env.str('DEFAULT_SUPERUSER_PASSWORD')
default_is_active: bool = True
default_is_superuser: bool = True


async def create_superuser(
        username: str = default_superuser_username,
        email: EmailStr = default_superuser_email,
        password: str = default_superuser_password,
        is_active: bool = default_is_active,
        is_superuser: bool = default_is_superuser,
) -> None:
    existing_user = await UserRepo.check_existing_user(username=username, email=email)
    if existing_user:
        if existing_user.username == username:
            raise AlreadyExistsException('Username')
        if existing_user.email == email:
            raise AlreadyExistsException('Email')
    password = get_password_hash(password=password)
    await UserRepo.create_one(
        username=username,
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    print(f'Superuser credentials: username: {username}, email: {email}, password: {password}')


if __name__ == '__main__':
    asyncio.run(create_superuser())
