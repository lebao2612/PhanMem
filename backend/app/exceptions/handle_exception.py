from typing import Any

class HandledException(Exception):
    def __init__(self, message: str, code: int = 400, details: Any = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(message)
