# type: ignore[attr-defined]
import os

import uvicorn

from image_service.logger_config import logger  # type: ignore[attr-defined]


@logger.catch()
def main() -> None:
    from image_service.app import image_app  # pylint: disable=import-outside-toplevel
    app = image_app
    port = int(os.environ.get("PORT", 5555))
    logger.info("Starting uvicorn!")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")


if __name__ == "__main__":
    main()
