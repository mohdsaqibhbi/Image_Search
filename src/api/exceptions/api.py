class APIBaseException(Exception):
    def __init__(self, message: str, status_code: int = 500) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class APIInternalError(APIBaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)