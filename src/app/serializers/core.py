from app.repositories import BaseRepository


class RepositorySerializerMixin:
    repository_classes = {}

    def get_repository(self, repository_name: str) -> type[BaseRepository]:
        return self._get_repository_class(repository_name)

    def _get_repository_class(self, repository_name: str) -> type[BaseRepository]:
        return self.repository_classes.get(repository_name)()
