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
image_app.mount("/static", StaticFiles(directory="static"), name="static")
