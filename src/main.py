from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.categories.routers import categories_router
from src.config import settings
from src.database import database_manager
from src.users.routers import auth_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database_manager.dispose_engine()


def app_factory() -> FastAPI:
    app = FastAPI(
        title=settings.app.project_name,
        version=settings.app.project_version,
        debug=settings.app.project_debug,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    return app


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app_factory',
        host=settings.app.project_host,
        port=settings.app.project_port,
        factory=True,
        reload=True,
    )
