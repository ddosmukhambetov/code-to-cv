from passlib.context import CryptContext

from app.users.repos import UserRepo

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await UserRepo.get_one_or_none(username=username, is_active=True)
    if not user or not verify_password(password, user.password):
        return None
    return user
