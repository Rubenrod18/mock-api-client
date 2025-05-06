from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request

from app import serializers, swagger as swagger_models
from app.blueprints.base import BaseResource
from app.di_container import ServiceDIContainer
from app.extensions import api as root_api
from app.services.post import PostService

blueprint = Blueprint('posts', __name__)
api = root_api.namespace('posts', description='CRUD endpoints.')


class BasePostResource(BaseResource):
    @inject
    def __init__(
        self,
        rest_api: str,
        service: PostService = Provide[ServiceDIContainer.post_service],
        *args,
        **kwargs,
    ):
        super().__init__(rest_api, service, *args, **kwargs)


@api.route('')
class NewPostResource(BasePostResource):
    serializer_class = serializers.PostSerializer

    @api.doc(responses={422: 'Unprocessable Entity'})
    @api.expect(swagger_models.post_input_sw_model)
    @api.marshal_with(swagger_models.post_sw_model, envelope='data', code=201)
    def post(self) -> tuple:
        """Create a post in JSONPlaceholder API and save it in database."""
        serializer = self.get_serializer()
        validated_data = serializer.load(request.get_json())

        post = self.service.create(**validated_data)

        return serializer.dump(post), 201

    @api.marshal_with(swagger_models.post_sw_model, envelope='data', code=200, as_list=True)
    def get(self) -> tuple:
        """Get the records from database."""
        serializer = self.get_serializer(**{'many': True})

        posts = self.service.get()

        return serializer.dump(posts), 200


@api.route('/<int:post_id>')
class PostResource(BasePostResource):
    serializer_class = serializers.PostSerializer

    @api.doc(responses={422: 'Unprocessable Entity'})
    @api.marshal_with(swagger_models.post_sw_model, envelope='data')
    def get(self, post_id: int) -> tuple:
        """Get a post from JSONPlaceholder API."""
        serializer = self.get_serializer()
        serializer.load({'id': post_id}, partial=True)

        post = self.service.find(post_id)

        return serializer.dump(post), 200

    @api.doc(responses={422: 'Unprocessable Entity'})
    @api.expect(swagger_models.post_patch_input_sw_model)
    @api.marshal_with(swagger_models.post_sw_model, envelope='data')
    def patch(self, post_id: int) -> tuple:
        """Update partially a post from JSONPlaceholder API."""
        json_data = request.get_json()
        serializer = self.get_serializer()
        deserialized_data = serializer.load(json_data)

        post = self.service.save(post_id, **deserialized_data)

        return serializer.dump(post), 200

    @api.doc(responses={422: 'Unprocessable Entity'})
    @api.marshal_with({})
    def delete(self, post_id: int) -> tuple:
        """Delete a post from JSONPlaceholder API."""
        serializer = self.get_serializer()
        serializer.load({'id': post_id}, partial=True)

        post = self.service.delete(post_id)

        return serializer.dump(post), 200
