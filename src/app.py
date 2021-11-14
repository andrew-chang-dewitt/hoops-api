"""API server."""

from typing import Awaitable, Callable

from fastapi import FastAPI, status as http_status, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from .config import Config
from .database import create_client
from .routers import status, create_transaction


def create_app(config: Config = Config()) -> FastAPI:
    """Application factory, create new server with given configuration."""
    database = create_client(config.database)
    app = FastAPI()

    @app.on_event("startup")
    async def startup() -> None:
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await database.disconnect()

    @app.middleware("http")
    async def post_must_be_json(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.method == "POST":
            if request.headers['content-type'] != 'application/json':
                return JSONResponse(
                    "Request Content-Type must be application/json.", 415)

        return await call_next(request)

    app.include_router(status)
    app.include_router(create_transaction(database))

    return app
