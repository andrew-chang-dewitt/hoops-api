"""
Hoops - A Web API for a personal budgeting application.

Run by either calling `python -m hoops.app` or 
`python -m flask` from the directory this file is in.

© 2021 Andrew Chang-DeWitt
Source distributed under an MIT License.
"""
from dataclasses import dataclass

from flask import Flask

# database
from .database import create_client, SyncClient
# route handlers
from .status import status
from .transactions import create_transactions


@dataclass
class Config:
    """
    Options that can be passed when creating the application.

    Provides sane defaults that can be overridden on creation.
    """

    # indicate that the application is created for testing only
    testing: bool = False
    database: SyncClient = create_client()


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

    # register route handlers
    app.register_blueprint(status)
    app.register_blueprint(create_transactions(db_client))

    return app
