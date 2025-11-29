import pytest

from app.utils.aws_sigv4 import create_signature_v4


def test_signature_v4_basic():
    method = "GET"
    url = "https://s3.amazonaws.com/test-bucket/test-key"
    headers = {}
    payload = b""
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    signed_headers = create_signature_v4(
        method, url, headers, payload, access_key, secret_key, "us-east-1"
    )
    
    assert "Authorization" in signed_headers
    assert "x-amz-date" in signed_headers
    assert "AWS4-HMAC-SHA256" in signed_headers["Authorization"]


def test_signature_v4_put_request():
    method = "PUT"
    url = "https://s3.amazonaws.com/test-bucket/test-key"
    headers = {}
    payload = b"test data"
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    signed_headers = create_signature_v4(
        method, url, headers, payload, access_key, secret_key, "us-east-1"
    )
    
    assert "Authorization" in signed_headers
    assert "x-amz-content-sha256" in signed_headers
    assert "content-length" in signed_headers


def test_signature_v4_different_regions():
    url = "https://s3.amazonaws.com/test-bucket/test-key"
    headers = {}
    payload = b""
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    us_east = create_signature_v4("GET", url, headers, payload, access_key, secret_key, "us-east-1")
    eu_west = create_signature_v4("GET", url, headers, payload, access_key, secret_key, "eu-west-1")
    
    assert us_east["Authorization"] != eu_west["Authorization"]

