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


class APIImageAlreadyExists(APIError):
    status_code = 409

    def __init__(self, image_name: str):
        super().__init__(f"Image with {image_name} name already exists. Please, choose other name.")


class APIImageWrongFormat(APIError):
    status_code = 422

    def __init__(self):  # type: ignore
        super().__init__("Wrong image format. Image format should be JPEG or PNG.")


class APIImageMaxSizeExceeded(APIError):
    status_code = 422

    def __init__(self, max_size: int):
        super().__init__(f"Max image size should be less than {max_size} MB.")
