import os
import re
from pathlib import Path

import aiofiles
from aiofiles import os as aios

from app.storage.base import StorageBackend
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


class LocalStorageBackend(StorageBackend):
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _sanitize_id(self, blob_id: str) -> str:
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', blob_id)
        sanitized = re.sub(r'\.\.', '_', sanitized)
        return sanitized

    def _get_file_path(self, blob_id: str) -> Path:
        sanitized = self._sanitize_id(blob_id)
        return self.storage_path / sanitized

    async def store(self, blob_id: str, data: bytes) -> None:
        try:
            file_path = self._get_file_path(blob_id)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(data)
        except Exception as e:
            raise StorageBackendError(f"Failed to store blob: {str(e)}") from e

    async def retrieve(self, blob_id: str) -> bytes:
        try:
            file_path = self._get_file_path(blob_id)
            if not await aios.path.exists(file_path):
                raise BlobNotFoundError(f"Blob {blob_id} not found")
            
            async with aiofiles.open(file_path, 'rb') as f:
                return await f.read()
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise StorageBackendError(f"Failed to retrieve blob: {str(e)}") from e

    async def exists(self, blob_id: str) -> bool:
        try:
            file_path = self._get_file_path(blob_id)
            return await aios.path.exists(file_path)
        except Exception as e:
            raise StorageBackendError(f"Failed to check blob existence: {str(e)}") from e

    async def delete(self, blob_id: str) -> None:
        try:
            file_path = self._get_file_path(blob_id)
            if await aios.path.exists(file_path):
                await aios.remove(file_path)
        except Exception as e:
            raise StorageBackendError(f"Failed to delete blob: {str(e)}") from e

