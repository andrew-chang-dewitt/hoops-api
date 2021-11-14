"""Application config."""

import os
from dataclasses import dataclass

from .database import create_conn_config, ConnectionParameters


@dataclass
class Config:
    """Application configuration object."""

    database: ConnectionParameters = create_conn_config(
        user=os.getenv('DB_USER', 'test'),
        password=os.getenv('DB_PASS', 'pass'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        database=os.getenv('DB_NAME', 'dev'))
