"""Application config."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from .database import create_conn_config, ConnectionParameters


load_dotenv(".secrets")


def get_app_key() -> str:
    """Get application key from environment."""
    key = os.getenv("APP_KEY")

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
