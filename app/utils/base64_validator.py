"""Base64 validation and decoding utilities."""

import base64

from app.utils.exceptions import InvalidBase64Error


def validate_base64(data: str) -> None:
    """Validate Base64 string format."""
    if not data:
        raise InvalidBase64Error("Base64 string cannot be empty")
    
    try:
        base64.b64decode(data, validate=True)
    except Exception as e:
        raise InvalidBase64Error(f"Invalid Base64 encoding: {str(e)}") from e


def decode_base64(data: str) -> bytes:
    """Decode Base64 string to bytes."""
    if not data:
        raise InvalidBase64Error("Base64 string cannot be empty")
    
    try:
        return base64.b64decode(data)
    except Exception as e:
        raise InvalidBase64Error(f"Invalid Base64 encoding: {str(e)}") from e

