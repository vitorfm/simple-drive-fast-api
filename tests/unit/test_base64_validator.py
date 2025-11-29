import pytest

from app.utils.base64_validator import decode_base64, validate_base64
from app.utils.exceptions import InvalidBase64Error


def test_valid_base64_strings():
    valid_cases = [
        ("SGVsbG8gV29ybGQ=", b"Hello World"),
        ("SGVsbG8=", b"Hello"),
        ("SGVsbG8gU2ltcGxlIFN0b3JhZ2UgV29ybGQh", b"Hello Simple Storage World!"),
    ]
    for encoded, expected in valid_cases:
        result = decode_base64(encoded)
        assert result == expected


def test_invalid_base64_strings():
    invalid_cases = [
        "SGVsbG8gV29ybGQ",
        "SGVsbG8gV29ybGQ==",
        "SGVsbG8!V29ybGQ=",
        "SGVsbG8@V29ybGQ=",
        "Not Base64!",
    ]
    for invalid in invalid_cases:
        with pytest.raises(InvalidBase64Error):
            validate_base64(invalid)


def test_empty_string():
    with pytest.raises(InvalidBase64Error):
        validate_base64("")


def test_unicode_utf8_data():
    text = "Hello 世界"
    import base64
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    result = decode_base64(encoded)
    assert result == text.encode("utf-8")


def test_binary_data():
    binary_data = bytes(range(256))
    import base64
    encoded = base64.b64encode(binary_data).decode("utf-8")
    result = decode_base64(encoded)
    assert result == binary_data


def test_padding_variations():
    valid_with_padding = "SGVsbG8="
    assert decode_base64(valid_with_padding) == b"Hello"

