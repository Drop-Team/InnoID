import uuid

from .entities import App
from .errors import AppNotFoundError
from .repositories import IAppRepository


class AppUseCase:
    app_repository: IAppRepository

    def __init__(self, app_repository: IAppRepository):
        self.app_repository = app_repository

    def get_by_id(self, app_id: uuid.UUID) -> App:
        app = self.app_repository.get_by_id(app_id)
        if not app:
            raise AppNotFoundError()
        return app

    def get_list(self, offset: int = 0, limit: int = 100) -> list[App]:
        return self.app_repository.get_list(offset, limit)

    def create(self, name: str, owner_id: uuid.UUID) -> App:
        app = App(
            app_id=self.app_repository.next_id(),
            name=name,
            owner_id=owner_id,
        )
        app = self.app_repository.add(app)
        return app

    def delete(self, app_id: uuid.UUID) -> App:
        app = self.app_repository.remove(app_id)
        if not app:
            raise AppNotFoundError()
        return app
