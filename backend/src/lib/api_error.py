"""APIError class"""


class APIError(Exception):
    """Class to handle custom API exception"""

    def __init__(self, status_code: int, code: str):
        self.status_code = status_code
        self.code = code
