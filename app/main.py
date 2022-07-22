from fastapi import FastAPI

from app import setup
from app.config import config


def create_app() -> FastAPI:
    app = FastAPI(title=config.APP_TITLE)

    setup.setup_logging()
    setup.setup_error_reporting()
    setup.setup_error_handler(app)
    setup.setup_routes(app)
    setup.setup_middlewares(app)

    return app
