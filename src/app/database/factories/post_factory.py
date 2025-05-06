import factory

from app.database.factories.base_factory import BaseFactory
from app.models import Post


class PostFactory(BaseFactory):
    class Meta:
        model = Post

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Sequence(lambda n: f'title_{n}')
    body = factory.Faker('sentence')
    userId = factory.Sequence(lambda n: n + 1)
