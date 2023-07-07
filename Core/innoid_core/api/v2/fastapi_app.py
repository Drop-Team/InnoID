from fastapi.applications import FastAPI

from .app.routers import apps_router
from .auth.routers import auth_router
from .middlewares import ExceptionsMiddleware
from .profile.routers import profile_router


def get_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(ExceptionsMiddleware)

    app.include_router(profile_router)
    app.include_router(apps_router)
    app.include_router(auth_router)

    return app
