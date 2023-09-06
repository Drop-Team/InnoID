from fastapi.applications import FastAPI

from api.v2.routers import login_router, profile_router, apps_router, service_router
from .middlewares import ExceptionsMiddleware


def get_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(ExceptionsMiddleware)

    app.include_router(login_router)
    app.include_router(profile_router)
    app.include_router(apps_router)
    app.include_router(service_router)

    return app
