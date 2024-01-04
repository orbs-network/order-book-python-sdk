class Error(Exception):
    """Base class for exceptions in this module."""


class ErrUnauthorized(Error):
    """Raised when the provided API key is invalid."""


class ErrInvalidSymbolFormat(Error):
    """Raised when the provided symbol is invalid."""


class ErrInvalidToken(Error):
    """Raised when a token in the provided symbol pair is invalid."""


class ErrInvalidSide(Error):
    """Raised when the provided side is invalid."""


class ErrDecimalPlaces(Error):
    """Raised when the provided value has too many decimal places."""
