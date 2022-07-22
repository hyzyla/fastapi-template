import logging

from fastapi import APIRouter, FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app import error_reporting
from app.config import config
from app.errors import BaseError
from app.health import handlers as health
from app.notes import handlers as notes


def setup_error_reporting() -> None:
    error_reporting.init(
        dsn=config.SENTRY_DSN,
        environment=config.ENVIRONMENT,
    )


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


def setup_error_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseError)
    async def exception_handler(_: Request, exc: BaseError) -> Response:
        return JSONResponse(
            status_code=exc.http_status,
            content={"message": exc.message},
        )


def setup_routes(app: FastAPI) -> None:
    api = APIRouter(prefix=config.BASE_API_PATH)
    api.include_router(notes.router)
    api.include_router(health.router)

    app.include_router(api)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(SentryAsgiMiddleware)
