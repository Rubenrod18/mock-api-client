from abc import ABC

from flask import session

from app.models import Base


class BaseRepository(ABC):
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, record_id: int, *args, **kwargs):
        raise NotImplementedError

    def find_by_id(self, record_id: int, *args, **kwargs):
        raise NotImplementedError


class SessionRepository(BaseRepository):
    def __init__(self, model: type[Base], session_key: str):
        super().__init__(model=model)
        self.session_key = session_key

    @property
    def session(self):
        return session.get(self.session_key, [])

    def create(self, **kwargs) -> dict:
        data = self.session
        data.append(kwargs)
        session[self.session_key] = data
        return kwargs

    def get(self, *args, **kwargs) -> list[dict | None]:
        return self.session

    def find_by_id(self, record_id: int, *args, **kwargs) -> dict | None:
        return next((item for item in self.session if item['id'] == record_id), None)

    def save(self, record_id: int, *args, **kwargs) -> dict | bool:
        for item in self.session:
            if item['id'] == record_id:
                item.update(kwargs)
                return item

        return False
