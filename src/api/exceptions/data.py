from exceptions.api import APIBaseException

class DataBaseException(APIBaseException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

