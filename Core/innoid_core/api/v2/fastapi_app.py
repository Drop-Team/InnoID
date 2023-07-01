from fastapi.applications import FastAPI

from .middlewares import ExceptionsMiddleware
from .user.routers import users_router
from .app.routers import apps_router
from .auth.routers import auth_router


def get_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(ExceptionsMiddleware)

    app.include_router(users_router)
    app.include_router(apps_router)
    app.include_router(auth_router)

    return app
