import hashlib

import httpx

from app.storage.base import StorageBackend
from app.utils.aws_sigv4 import create_signature_v4
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


class S3CompatibleStorageBackend(StorageBackend):
    def __init__(
        self,
        endpoint_url: str,
        bucket_name: str,
        access_key_id: str,
        secret_access_key: str,
        region: str = "us-east-1",
    ):
        self.endpoint_url = endpoint_url.rstrip("/")
        self.bucket_name = bucket_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.client = httpx.AsyncClient()

    def _get_url(self, blob_id: str) -> str:
        return f"{self.endpoint_url}/{self.bucket_name}/{blob_id}"

    def _get_headers(self, method: str, url: str, payload: bytes) -> dict[str, str]:
        headers = {
            "host": httpx.URL(url).host or "",
            "x-amz-content-sha256": hashlib.sha256(payload).hexdigest(),
        }
        if payload:
            headers["content-length"] = str(len(payload))
        return create_signature_v4(
            method,
            url,
            headers,
            payload,
            self.access_key_id,
            self.secret_access_key,
            self.region,
        )

    async def store(self, blob_id: str, data: bytes) -> None:
        url = self._get_url(blob_id)
        headers = self._get_headers("PUT", url, data)
        
        try:
            response = await self.client.put(url, content=data, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise StorageBackendError(f"S3 store failed: {e.response.status_code}") from e
        except Exception as e:
            raise StorageBackendError(f"S3 store error: {str(e)}") from e

    async def retrieve(self, blob_id: str) -> bytes:
        url = self._get_url(blob_id)
        headers = self._get_headers("GET", url, b"")
        
        try:
            response = await self.client.get(url, headers=headers)
            if response.status_code == 404:
                raise BlobNotFoundError(f"Blob {blob_id} not found")
            response.raise_for_status()
            return response.content
        except BlobNotFoundError:
            raise
        except httpx.HTTPStatusError as e:
            raise StorageBackendError(f"S3 retrieve failed: {e.response.status_code}") from e
        except Exception as e:
            raise StorageBackendError(f"S3 retrieve error: {str(e)}") from e

    async def exists(self, blob_id: str) -> bool:
        url = self._get_url(blob_id)
        headers = self._get_headers("HEAD", url, b"")
        
        try:
            response = await self.client.head(url, headers=headers)
            return response.status_code == 200
        except Exception:
            return False

    async def delete(self, blob_id: str) -> None:
        url = self._get_url(blob_id)
        headers = self._get_headers("DELETE", url, b"")
        
        try:
            response = await self.client.delete(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise StorageBackendError(f"S3 delete error: {str(e)}") from e

