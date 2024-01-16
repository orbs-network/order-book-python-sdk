class Error(Exception):
    """Base class for exceptions in this module."""


class ErrUnauthorized(Error):
    """Raised when the provided API key is invalid."""


class ErrApiRequest(Error):
    """Raised when an API request fails"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP Error {status_code}: {message}")


class ErrInvalidSymbolFormat(Error):
    """Raised when the provided symbol is invalid."""


class ErrInvalidToken(Error):
    """Raised when a token in the provided symbol pair is invalid."""


class ErrInvalidSide(Error):
    """Raised when the provided side is invalid."""


class ErrDecimalPlaces(Error):
    """Raised when the provided value has too many decimal places."""
