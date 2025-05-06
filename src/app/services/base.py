from abc import ABC, abstractmethod

from app.repositories import BaseRepository


class ProviderServiceMixin:
    def __init__(self, repository: BaseRepository, provider):
        self.provider = provider
        self.repository = repository


class BaseService(ABC):
    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def find(self, record_id: int, *args):
        raise NotImplementedError

    @abstractmethod
    def save(self, record_id: int, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id: int):
        raise NotImplementedError
