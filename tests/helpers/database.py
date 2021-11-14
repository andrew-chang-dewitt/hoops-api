"""Test helper methods."""

from typing import Any, TypeVar
from unittest.mock import Mock

from db_wrapper.model import (
    ModelData,
    AsyncModel,
)

from src.database import ConnectionParameters, Client


def mock_client() -> Client:
    """Return a mocked client instance."""
    conn_params = ConnectionParameters('a', 0, 'a', 'a', 'a')

    return Mock(Client(conn_params))


AnyModelData = TypeVar('AnyModelData', bound=ModelData)
AnyAsyncModel = TypeVar('AnyAsyncModel', bound=AsyncModel[Any])


def mock_model(model: AnyAsyncModel) -> AnyAsyncModel:
    """Return a mocked model instance."""
    create = Mock(spec=model.create)
    read = Mock(spec=model.read)
    update = Mock(spec=model.update)
    delete = Mock(spec=model.delete)

    model = Mock(spec=model)
    model.create = create
    model.read = read
    model.update = update
    model.delete = delete

    return model
