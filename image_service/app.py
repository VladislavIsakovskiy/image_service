import os
from os.path import join as path_join

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from loguru import logger

from starlette.responses import HTMLResponse


def create_app() -> FastAPI:
    logger.info("Starting image service app!")
    app = FastAPI(
        title="Image service app",
        description="API for image service app",
        default_response_class=HTMLResponse
    )

    return app


image_app = create_app()

current_dir = os.path.dirname(os.path.abspath(__file__))

image_app.mount("/static", StaticFiles(directory=path_join(current_dir, "..", "static")), name="static")
