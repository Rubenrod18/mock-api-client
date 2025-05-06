"""Registers third party extensions."""

from flask import Flask
from flask_marshmallow import Marshmallow

from app.helpers.custom_api import CustomApi
from flask_session import Session

ma = Marshmallow()
session = Session()
api = CustomApi(
    prefix='/api',
    title='mock-api-client',
    description='A simple description',
)


def init_app(app: Flask) -> None:
    api.init_app(app)
    ma.init_app(app)
    session.init_app(app)
    _init_python_dependency_injector(app)


def _init_python_dependency_injector(flask_app: Flask) -> None:
    from app.di_container import ServiceDIContainer

    container = ServiceDIContainer()
    flask_app.container = container
