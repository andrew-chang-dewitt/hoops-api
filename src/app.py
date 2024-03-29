"""API server."""

from typing import Awaitable, Callable, Optional

from fastapi import FastAPI, status as http_status, Request, Response
from fastapi.responses import JSONResponse

from .config import create_default_config, Config
from .database import create_client, NoResultFound
from .routers import (
    status,
    create_account,
    create_balance,
    create_envelope,
    create_token,
    create_transaction,
    create_user,
)


def create_app(config: Optional[Config] = None) -> FastAPI:
    """Application factory, create new server with given configuration."""
    if config is None:
        config = create_default_config()

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
        if req.method == "POST":
            last_six = req.url.path[len(req.url.path) - 6:]

            if last_six != "/token":
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
                }
            }
        )

    app.include_router(status)
    app.include_router(create_user(config, database))
    app.include_router(create_token(config, database))
    app.include_router(create_account(config, database))
    app.include_router(create_transaction(config, database))
    app.include_router(create_balance(config, database))
    app.include_router(create_envelope(config, database))

    return app
