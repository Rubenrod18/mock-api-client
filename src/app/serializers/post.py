import logging

from marshmallow import fields, validates
from werkzeug.exceptions import NotFound

from app.extensions import ma
from app.models import Post
from app.repositories.post import PostRepository
from app.serializers.core import RepositorySerializerMixin

logger = logging.getLogger(__name__)


class PostSerializer(ma.Schema, RepositorySerializerMixin):
    class Meta:
        model = Post
        ordered = True

    repository_classes = {'post_repository': PostRepository}

    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    userId = fields.Integer(data_key='user_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._post_repository = self.get_repository('post_repository')

    @validates('id')
    def validate_id(self, post_id: int):
        post = self._post_repository.find_by_id(record_id=post_id)

        if not post:
            logger.debug(f'Post "{post_id}" not found.')
            raise NotFound('Post not found')
