class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class ErrInvalidSymbolFormat(Error):
    """Raised when the provided symbol is invalid."""

    pass


class ErrInvalidToken(Error):
    """Raised when a token in the provided symbol pair is invalid."""

    pass


class ErrInvalidSide(Error):
    """Raised when the provided side is invalid."""

    pass
