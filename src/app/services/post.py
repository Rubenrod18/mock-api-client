from app.models import Post
from app.providers import JSONPlaceholderProvider
from app.repositories.post import PostRepository
from app.services.base import BaseService, ProviderServiceMixin


class PostService(BaseService, ProviderServiceMixin):
    def __init__(self):
        super().__init__(provider=JSONPlaceholderProvider(), repository=PostRepository())

    def create(self, **kwargs) -> Post:
        api_post = self.provider.post.create(kwargs)
        post = self.repository.create(**api_post)
        return post

    def find(self, record_id: int, *args) -> dict:
        return self.provider.post.find_by_id(record_id)

    def get(self, **kwargs) -> list[Post | None]:
        return self.repository.get()

    def save(self, record_id: int, **kwargs) -> Post:
        return self.provider.post.patch(post_id=record_id, payload=kwargs)

    def delete(self, record_id: int) -> dict:
        return self.provider.post.delete(record_id)
