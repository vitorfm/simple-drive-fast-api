import os

import aioftp

from app.storage.base import StorageBackend
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


class FTPStorageBackend(StorageBackend):
    def __init__(
        self,
        host: str,
        port: int = 21,
        username: str = "anonymous",
        password: str = "",
        base_dir: str = "/",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_dir = base_dir.rstrip("/") or "/"
        self.client: aioftp.Client | None = None

    async def _ensure_connected(self) -> None:
        if self.client is None:
            try:
                self.client = aioftp.Client()
                await self.client.connect(self.host, self.port)
                await self.client.login(self.username, self.password)
                if self.base_dir != "/":
                    try:
                        await self.client.change_directory(self.base_dir)
                    except Exception:
                        await self.client.make_directory(self.base_dir)
                        await self.client.change_directory(self.base_dir)
            except Exception as e:
                raise StorageBackendError(f"Failed to connect to FTP server: {e}") from e

    def _get_path(self, blob_id: str) -> str:
        if self.base_dir == "/":
            return blob_id
        return f"{self.base_dir}/{blob_id}".replace("//", "/")

    async def store(self, blob_id: str, data: bytes) -> None:
        await self._ensure_connected()
        if self.client is None:
            raise StorageBackendError("FTP client not connected")
        
        try:
            path = self._get_path(blob_id)
            data_stream = BytesIO(data)
            await self.client.upload_stream(path, data_stream)
        except Exception as e:
            raise StorageBackendError(f"Failed to store blob {blob_id} via FTP: {e}") from e

    async def retrieve(self, blob_id: str) -> bytes:
        await self._ensure_connected()
        if self.client is None:
            raise StorageBackendError("FTP client not connected")
        
        try:
            path = self._get_path(blob_id)
            if not await self.exists(blob_id):
                raise BlobNotFoundError(f"Blob {blob_id} not found on FTP server")
            
            data_stream = BytesIO()
            await self.client.download_stream(path, data_stream)
            data_stream.seek(0)
            return data_stream.read()
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise StorageBackendError(f"Failed to retrieve blob {blob_id} via FTP: {e}") from e

    async def exists(self, blob_id: str) -> bool:
        await self._ensure_connected()
        if self.client is None:
            return False
        
        try:
            path = self._get_path(blob_id)
            files = await self.client.list()
            filename = os.path.basename(path)
            for file_info in files:
                if file_info.name == filename:
                    return True
            return False
        except Exception:
            return False

    async def delete(self, blob_id: str) -> None:
        await self._ensure_connected()
        if self.client is None:
            raise StorageBackendError("FTP client not connected")
        
        try:
            path = self._get_path(blob_id)
            await self.client.remove_file(path)
        except Exception as e:
            raise StorageBackendError(f"Failed to delete blob {blob_id} via FTP: {e}") from e

