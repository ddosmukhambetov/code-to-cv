from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import UserAdmin
from app.core.config import settings
from app.core.database import database_manager
from app.users.auth.routers import router as auth_router
from app.users.routers import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database_manager.dispose_engine()


def app_factory() -> FastAPI:
    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        debug=settings.app.debug,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )

    app.include_router(auth_router)
    app.include_router(users_router)

    admin = Admin(app, engine=database_manager.engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    return app


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app_factory',
        host=settings.app.host,
        port=settings.app.port,
        factory=True,
        reload=True,
    )
