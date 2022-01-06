class APIError(Exception):
    status_code: int = None  # type: ignore
    message: str = None  # type: ignore

    def __init__(self, message: str = None):
        super().__init__(message)
        if message:
            self.message = message


class APIImageNotFound(APIError):
    status_code = 422

    def __init__(self, image_name: str):
        super().__init__(f"There is no image {image_name} at server.")


class APIImageNotDeleted(APIError):
    status_code = 422

    def __init__(self, image_name: str):
        super().__init__(f"Something went wrong with deleting {image_name} image.")
