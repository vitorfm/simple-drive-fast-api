import hashlib
import hmac
from datetime import datetime
from urllib.parse import quote, urlparse


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _hmac_sha256(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


def _url_encode(s: str, safe: str = "/") -> str:
    return quote(s, safe=safe)


def _canonical_headers(headers: dict[str, str]) -> tuple[str, str]:
    sorted_headers = sorted(headers.items())
    canonical = "\n".join(f"{k.lower()}:{v.strip()}" for k, v in sorted_headers)
    signed = ";".join(k.lower() for k, _ in sorted_headers)
    return canonical, signed


def _canonical_request(
    method: str,
    uri: str,
    query: str,
    headers: dict[str, str],
    payload_hash: str,
) -> str:
    canonical_uri = uri
    canonical_querystring = query
    canonical_headers_str, signed_headers = _canonical_headers(headers)
    
    return f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers_str}\n\n{signed_headers}\n{payload_hash}"


def _string_to_sign(
    timestamp: str,
    date_stamp: str,
    region: str,
    service: str,
    canonical_request: str,
) -> str:
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()
    return f"AWS4-HMAC-SHA256\n{timestamp}\n{scope}\n{canonical_request_hash}"


def _get_signature_key(
    secret_key: str,
    date_stamp: str,
    region: str,
    service: str,
) -> bytes:
    k_date = _hmac_sha256(f"AWS4{secret_key}".encode(), date_stamp.encode())
    k_region = _hmac_sha256(k_date, region.encode())
    k_service = _hmac_sha256(k_region, service.encode())
    k_signing = _hmac_sha256(k_service, b"aws4_request")
    return k_signing


def create_signature_v4(
    method: str,
    url: str,
    headers: dict[str, str],
    payload: bytes,
    access_key: str,
    secret_key: str,
    region: str = "us-east-1",
    service: str = "s3",
) -> dict[str, str]:
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    
    parsed = urlparse(url)
    uri = parsed.path or "/"
    query = parsed.query
    
    payload_hash = hashlib.sha256(payload).hexdigest()
    
    if "x-amz-date" not in headers:
        headers["x-amz-date"] = timestamp
    if "host" not in headers:
        headers["host"] = parsed.netloc
    
    canonical_req = _canonical_request(method, uri, query, headers, payload_hash)
    string_to_sign = _string_to_sign(timestamp, date_stamp, region, service, canonical_req)
    
    signing_key = _get_signature_key(secret_key, date_stamp, region, service)
    signature = _hmac_sha256(signing_key, string_to_sign.encode()).hexdigest()
    
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    auth_header = f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, SignedHeaders={_canonical_headers(headers)[1]}, Signature={signature}"
    
    headers["Authorization"] = auth_header
    return headers

