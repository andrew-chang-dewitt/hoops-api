from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)
from uuid import UUID

from asgi_lifespan import LifespanManager
from fastapi import FastAPI, Header
from httpx import AsyncClient

from tests.helpers.database import get_test_db

from src import create_app
from src.config import Config as AppConfig
from src.database import Client

AppGetter = Tuple[FastAPI, Client]

BASE_URL = "http://localhost:8000"


def _add_test_routes(
    app: FastAPI,
    routes: List[Tuple[str, str, Callable[..., Any]]]
) -> FastAPI:
    for method, path, handler in routes:
        getattr(app, method)(path)(handler)

    return app


def get_test_app(
    routes: List[Tuple[str, str, Callable[..., Any]]]
) -> Callable[[], Awaitable[AppGetter]]:
    async def getter() -> Tuple[FastAPI, Client]:
        db_config, db_client = await get_test_db()

        test_config = AppConfig(
            database=db_config)
        test_app = create_app(test_config)
        test_app_with_routes = _add_test_routes(test_app, routes)

        return test_app_with_routes, db_client
    return getter


def get_fake_auth_token(user_id: UUID) -> str:
    """'Encode' a user_id into a fake JWT & return it."""
    return f"Bearer {str(user_id)}"


async def mock_get_active_user(authorization: str = Header(None)) -> UUID:
    """Mock src.security.get_active_user."""
    token = authorization[7:]
    print("getting user from mock token:", token)
    return UUID(token)


@asynccontextmanager
async def get_test_client(
    getter: Callable[..., Awaitable[Tuple[FastAPI, Client]]] = get_test_app([
    ]),
    dependency_overrides: Dict[Any, Any] = {}
) -> AsyncGenerator[Tuple[AsyncClient, Client], None]:
    """Create test client for application with lifecycle events."""
    app, database = await getter()

    for actual, mock in dependency_overrides.items():
        app.dependency_overrides[actual] = mock

    async with AsyncClient(
        app=app, base_url=BASE_URL
    ) as test_client, LifespanManager(app):
        yield test_client, database
