import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from loguru import logger

from starlette.responses import HTMLResponse

load_dotenv()
LOG_FOLDER = os.environ.get("DATA_FOLDER")

logger.add(f"{LOG_FOLDER}/debug.log", format="{time} {level} {message}", filter="image_service", level="DEBUG",
           rotation="5 MB")


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
