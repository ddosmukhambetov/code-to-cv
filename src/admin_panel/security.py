from typing import Annotated

from fastapi import Depends
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src import User
from src.config import settings
from src.users.dependencies import get_current_superuser
from src.users.schemas import UserReadSchema
from src.users.security import authenticate_user, create_access_token


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user: User = await authenticate_user(username, password)
        if user:
            if user.is_superuser:
                access_token = create_access_token(data={'sub': str(username)})
                request.session.update({'token': access_token})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')
        if not token:
            return False
        user = Annotated[UserReadSchema, Depends(get_current_superuser)]
        if not user:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.app.sqladmin_secret_key)
