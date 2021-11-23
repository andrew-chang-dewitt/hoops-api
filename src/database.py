"""Database methods."""

from db_wrapper import AsyncClient as Client, ConnectionParameters
# import NoResultFound to re-export
from db_wrapper.model.base import NoResultFound  # pylint: disable=W0611


def create_conn_config(
    *,
    user: str = 'postgres',
    password: str = 'postgres',
    host: str = 'localhost',
    port: int = 5432,
    database: str = 'postgres',
) -> ConnectionParameters:
    """Create database Connection Parameters."""
    return ConnectionParameters(user=user,
                                password=password,
                                host=host,
                                port=port,
                                database=database)


def create_client(
    conn_params: ConnectionParameters
) -> Client:
    """Create & return a database client."""
    return Client(conn_params)
