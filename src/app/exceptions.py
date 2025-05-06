"""Module for managing exceptions."""

import logging
import traceback

from flask import current_app, Flask, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import InternalServerError

logger = logging.getLogger(__name__)


def init_app(app: Flask) -> None:
    app.register_error_handler(ValidationError, _handle_validation_error_exception)


def _handle_validation_error_exception(ex: ValidationError) -> tuple:
    """Handler ValidationError exception."""

    if current_app.config['TESTING'] is False:
        logger.exception(traceback.format_exc())

    return jsonify({'message': ex.normalized_messages()}), 422


class HttpClientError(InternalServerError):
    description = 'General HTTP request failure'


class ExternalApiError(InternalServerError):
    description = 'Failure when talking to an external API'
