"""Module for testing post blueprint."""

from unittest.mock import MagicMock, patch

from app.database.factories.post_factory import PostFactory
from app.providers.jsonplaceholder import _PostProvider
from tests.base.base_api_test import TestBaseApi


class TestCreatePostEndpoint(TestBaseApi):
    def setUp(self):
        super().setUp()
        self.base_path = f'{self.base_path}/posts'

    @patch('app.services.post.JSONPlaceholderProvider', spec=True)
    def test_create_post_endpoint(self, mock_provider_class):
        payload = PostFactory.build_dict(exclude={'id'})
        payload['user_id'] = payload['userId']
        payload.pop('userId')

        mock_post_provider = MagicMock(spec=_PostProvider)
        mock_post_provider.create.return_value = {
            'id': 101,
            'title': payload['title'],
            'body': payload['body'],
            'userId': payload['user_id'],
        }

        mock_provider_instance = MagicMock()
        mock_provider_instance.post = mock_post_provider
        mock_provider_class.return_value = mock_provider_instance

        response = self.client.post(f'{self.base_path}', json=payload)
        json_response = response.get_json()
        json_data = json_response.get('data')

        mock_post_provider.create.assert_called_once()
        self.assertEqual(201, response.status_code, response.data)
        self.assertTrue(101, json_data.get('id'))
        self.assertEqual(payload.get('title'), json_data.get('title'))
        self.assertEqual(payload.get('body'), json_data.get('body'))
        self.assertEqual(payload.get('user_id'), json_data.get('user_id'))
