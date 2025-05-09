import logging
import unittest

from dotenv import find_dotenv, load_dotenv
from flask import Flask, Response
from flask.testing import FlaskClient

logger = logging.getLogger(__name__)


class _CustomFlaskClient(FlaskClient):
    @staticmethod
    def __before_request(*args, **kwargs):
        logger.debug(f'args: {args}')
        logger.debug(f'kwargs: {kwargs}')

    @staticmethod
    def __log_request_data(response: Response):
        if response.mimetype == 'application/json' and response.data:
            response_data = response.get_json()
        else:
            response_data = response.data
        logger.debug(f'response data: {response_data}')

    def __after_request(self, response: Response):
        logger.debug(f'response status code: {response.status_code}')
        logger.debug(f'response mime type: {response.mimetype}')
        self.__log_request_data(response)

    def __make_request(self, method: str, *args, **kwargs):
        logger.debug('< === START REQUEST === >')
        self.__before_request(*args, **kwargs)

        kwargs['method'] = method
        response = self.open(*args, **kwargs)

        self.__after_request(response)
        logger.debug('< === END REQUEST === >')
        return response

    def get(self, *args, **kwargs):
        """Like open but method is enforced to GET."""
        return self.__make_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        """Like open but method is enforced to POST."""
        return self.__make_request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        """Like open but method is enforced to PUT."""
        return self.__make_request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Like open but method is enforced to DELETE."""
        return self.__make_request('DELETE', *args, **kwargs)


class TestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__engine = None
        self.app = None
        self.client = None
        self.runner = None
        self.session = None

    @classmethod
    def setUpClass(cls):
        """Load environment variables before running any test."""
        load_dotenv(find_dotenv('.env.test'), override=True)

    def setUp(self) -> None:
        app = self.__create_app()
        app_context = app.app_context()
        app_context.push()

        self.app = app
        self.client = self.__create_test_client(self.app)
        self.runner = self.app.test_cli_runner()

    @staticmethod
    def __create_app():
        """Create an app with testing environment."""
        from app import create_app

        return create_app('config.TestConfig')

    @staticmethod
    def __create_test_client(app: Flask):
        """Create a test client for making http requests."""
        app.test_client_class = _CustomFlaskClient
        return app.test_client()
