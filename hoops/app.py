"""
Hoops - A Web API for a personal budgeting application.

Run by either calling `python -m hoops.app` or
`python -m flask` from the directory this file is in.

© 2021 Andrew Chang-DeWitt
Source distributed under an MIT License.
"""
from dataclasses import dataclass
from datetime import date, datetime
import os
from typing import Any, Callable

from flask import jsonify, Flask
from flask.json import JSONEncoder
from flask.typing import ResponseReturnValue
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

# helpers
from .database import create_client, SyncClient, NoResultFound
from .response import ErrResponse
from .errors import BadRequest
# route handlers
from .transactions import create_transactions
from .status import status


def is_debug(env_value: str) -> bool:
    """Check if given value indicates to run app in DEBUG mode."""
    if env_value == '1':
        return True
    if env_value == '0':
        return False

    raise ValueError('Invalid value for FLASK_DEBUG environment variable.')


@dataclass
class Config:
    """
    Options that can be passed when creating the application.

    Provides sane defaults that can be overridden on creation.
    """

    database: SyncClient = create_client()
    debug: bool = is_debug(os.getenv('FLASK_DEBUG', '0'))


class ISODateJSONEncoder(JSONEncoder):
    """Custom json encoder that uses ISO date format for date & datetime."""

    def default(self, o: Any) -> Any:
        """Serialize the given object as JSON."""
        if isinstance(o, (date, datetime)):
            return o.isoformat()

        return super().default(o)


def create_app(config: Config = Config()) -> Flask:
    """
    Application factory.

    Uses default config options unless told otherwise.
    """
    #
    # DATABSE
    #
    db_client = config.database

    #
    # APP SETUP
    #

    # create app
    app = Flask(__name__)

    # fix jsonify's encodign to use ISO date format
    app.json_encoder = ISODateJSONEncoder

    # error handlers

    def create_err_handler(
        code: int
    ) -> Callable[[Exception], ResponseReturnValue]:
        """Build handler for any given error with given HTTP status code."""
        def generic_err_handler(err: Exception) -> ResponseReturnValue:
            """
            Handle given exception.

            Passes HTTPExceptions through unhandled to WSGI server.

            All other errors get formatted to standard ErrorResponse object
            before getting serialized as JSON to be returned by the API. If
            config.debug is truthy, then the stack trace is included in the
            response.
            """
            if isinstance(err, HTTPException):
                return err

            return (jsonify(ErrResponse.from_exception(err, config.debug)),
                    code)

        return generic_err_handler

    # 400 when a request is badly formed
    for err_type in BadRequest, ValidationError:
        app.register_error_handler(
            err_type, create_err_handler(400))  # type: ignore
    # 404 when database returns no results for a query
    # mypy can't infer type as fitting ErrorHandlerCallable protocol correctly
    app.register_error_handler(
        NoResultFound, create_err_handler(404))  # type: ignore
    # 500 for all others
    app.register_error_handler(
        Exception, create_err_handler(500))  # type: ignore

    # register route handlers
    app.register_blueprint(status)
    app.register_blueprint(create_transactions(db_client))

    return app
