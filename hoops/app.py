"""
Hoops - A Web API for a personal budgeting application.

Run by either calling `python -m hoops.app` or 
`python -m flask` from the directory this file is in.

© 2021 Andrew Chang-DeWitt
Source distributed under an MIT License.
"""
from dataclasses import dataclass
from typing import Any

from flask import Flask

from status import status
from transactions import transactions


@dataclass
class Config:
    """
    Options that can be passed when creating the application.

    Provides sane defaults that can be overridden on creation.
    """

    # indicate that the application is created for testing only
    TESTING: bool = False
    # pass the necessary database info to the application
    DATABASE: None = None


def create_app(config: Config = Config()) -> Flask:
    """
    Application factory.

    Uses default config options unless told otherwise.
    """
    app = Flask(__name__)

    app.register_blueprint(status)
    app.register_blueprint(transactions)

    return app


if __name__ == "__main__":
    create_app().run()
