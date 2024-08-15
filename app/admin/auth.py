from fastapi.requests import Request
from sqladmin.authentication import AuthenticationBackend

from app.core.config import settings
from app.users.auth.security import authenticate_user
from app.users.auth.tokens import create_access_token
from app.users.schemas import UserReadSchema


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user: UserReadSchema = await authenticate_user(username, password)
        if user:
            if user.is_superuser:
                access_token = await create_access_token(user=user)
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
        return True


authentication_backend = AdminAuth(secret_key=settings.admin.sqladmin_secret_key)
