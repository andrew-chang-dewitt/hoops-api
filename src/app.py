"""API server."""

from typing import Awaitable, Callable

from fastapi import FastAPI, status as http_status, Request, Response
from fastapi.responses import JSONResponse

from .config import Config
from .database import create_client, NoResultFound
from .routers import (
    status,
    create_user,
    create_token,
    create_account,
    # create_transaction,
)


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
        req: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if req.method == "POST" and req.url.path[:6] != "/token":
            if req.headers['content-type'] != 'application/json':
                return JSONResponse(
                    "Request Content-Type must be application/json.",
                    http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return await call_next(req)

    @app.exception_handler(NoResultFound)
    async def no_result_found_sends_404(
        req: Request,
        exc: NoResultFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                'error': str(exc),
                'request': {
                    'url': str(req.url),
                    'method': req.method,
                    'headers': str(req.headers),
                    'query_parameters': str(req.query_params),
                    # json decoder breaks on empty body
                    'body': await req.json() if await req.body() else None,
                }
            }
        )

    app.include_router(status)
    app.include_router(create_user(database))
    app.include_router(create_token(database))
    app.include_router(create_account(database))
    # app.include_router(create_transaction(database))

    return app
