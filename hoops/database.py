import os

from db_wrapper import ConnectionParameters, SyncClient


def create_client() -> SyncClient:
    """Initialize a database Client."""
    db_connection_params = ConnectionParameters(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        user=os.getenv('DB_USER', 'test'),
        password=os.getenv('DB_PASS', 'pass'),
        database=os.getenv('DB_NAME', 'dev'))

    return SyncClient(db_connection_params)
