"""Custom exceptions for Simple Drive API."""


class SimpleDriveError(Exception):
    """Base exception for Simple Drive."""

    pass


class InvalidBase64Error(SimpleDriveError):
    """Raised when Base64 string is invalid."""

    pass


class BlobNotFoundError(SimpleDriveError):
    """Raised when blob is not found."""

    pass


class BlobAlreadyExistsError(SimpleDriveError):
    """Raised when blob ID already exists."""

    pass


class StorageBackendError(SimpleDriveError):
    """Raised when storage backend operation fails."""

    pass

