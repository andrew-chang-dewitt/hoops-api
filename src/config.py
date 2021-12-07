"""Application config."""

import os
from dataclasses import dataclass

from .database import create_conn_config, ConnectionParameters


def _get_app_key_from_file() -> str:
    with open("/run/secrets/app_key", "r") as key_file:
        key = str(key_file.readline())
        print(f"app_key from file: {key}")
        return key

def get_app_key() -> str:
    """Get application key from environment."""
    key = os.getenv("APP_KEY", _get_app_key_from_file())

    if not key:
        raise ValueError("An APP_KEY environment variable is required.")

    return key


@dataclass
class Config:
    """Application configuration object."""

    database: ConnectionParameters
    jwt_key: str


def create_default_config() -> Config:
    return Config(
        database=create_conn_config(
            user=os.getenv('DB_USER', 'test'),
            password=os.getenv('DB_PASS', 'pass'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'dev')),
        jwt_key=get_app_key())
