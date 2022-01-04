# type: ignore[attr-defined]
import os
from os.path import join as path_join

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from loguru import logger

from image_service.endpoints import images
from image_service.errors import APIError


def create_app() -> FastAPI:
    logger.info("Starting image service app!")
    app = FastAPI(
        title="Image service app",
        description="API for image service app",
    )

    return app


image_app = create_app()

current_dir = os.path.dirname(os.path.abspath(__file__))
image_app.mount(
    "/static",
    StaticFiles(directory=path_join(current_dir, "..", "static")),
    name="static",
)


@image_app.exception_handler(Exception)
def global_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        content={"message": str(exc)},
    )


@image_app.exception_handler(APIError)
def api_exception_handler(_request: Request, exc: APIError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


image_app.include_router(images.router, prefix="/v1")
