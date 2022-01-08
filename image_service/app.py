# type: ignore[attr-defined]
import os
from os.path import join as path_join

from fastapi import FastAPI, Request, Response
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


@image_app.middleware("http")
async def request_log(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        if response.status_code < 400:
            level = "INFO"
        else:
            level = "WARNING"
        logger.log(level, f"{request.method} {request.url} Status code: {response.status_code}")
        return response
    except Exception as exc:  # noqa # pylint: disable=broad-except
        logger.exception(str(exc))
        return JSONResponse(
            content={"message": "Something went wrong!"},
        )


@image_app.exception_handler(APIError)
def api_exception_handler(_request: Request, exc: APIError) -> JSONResponse:
    logger.warning(exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


image_app.include_router(images.router, prefix="/v1")
