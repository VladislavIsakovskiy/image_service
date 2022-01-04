class APIError(Exception):
    status_code: int = None  # type: ignore
    message: str = None  # type: ignore

    def __init__(self) -> None:
        super().__init__(self.message)


class APIImageNotFound(APIError):
    status_code = 413
    message = "I'm a teapot"
