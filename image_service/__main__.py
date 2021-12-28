import os

import uvicorn

from image_service.app import image_app

app = image_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="127.0.0.1", port=5555, log_level="debug")
