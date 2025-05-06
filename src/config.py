"""Module loads the application's configuration.

The extension and custom configurations are defined here.

"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Default configuration options."""

    # Flask
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    SERVER_NAME = os.getenv('SERVER_NAME')

    # Flask-Session
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'top-secret'

    # Flask Swagger UI
    SWAGGER_URL = os.getenv('SWAGGER_URL', '/docs')
    SWAGGER_API_URL = os.getenv('SWAGGER_API_URL', f'http://{SERVER_NAME}/static/swagger.yaml')

    # Flask Restx
    RESTX_ERROR_404_HELP = False
    FLASK_RESTFUL_PREFIX = '/api'
    RESTX_MASK_SWAGGER = False

    # Mr Developer
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', logging.INFO)

    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')

    ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = f'{ROOT_DIRECTORY}/static'
    TEMPLATES_FOLDER = f'{ROOT_DIRECTORY}/templates'

    ALLOWED_CONTENT_TYPES = {'application/json'}


class ProdConfig(Config):
    """Production configuration options."""

    pass


class DevConfig(Config):
    """Development configuration options."""

    # Flask
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    """Testing configuration options."""

    # Flask
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

    # Flask Session
    SESSION_PERMANENT = False

    # Mr Developer
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', logging.DEBUG)
