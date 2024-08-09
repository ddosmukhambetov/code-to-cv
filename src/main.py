from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin

from src.admin_panel.security import authentication_backend
from src.admin_panel.views import UserAdmin, CategoryAdmin, QuestionAdmin, CvAdmin
from src.categories.routers import categories_router
from src.config import settings
from src.cvs.routers import cvs_router
from src.database import database_manager
from src.interview_simulations.routers import questions_router
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
    app.include_router(questions_router)
    app.include_router(cvs_router)

    admin = Admin(app, engine=database_manager.engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(CvAdmin)

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
