from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.blob_data import BlobData
from app.storage.base import StorageBackend
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


class DatabaseStorageBackend(StorageBackend):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def store(self, blob_id: str, data: bytes) -> None:
        try:
            blob_data = BlobData(id=blob_id, data=data)
            self.db_session.add(blob_data)
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise StorageBackendError(f"Failed to store blob: {str(e)}") from e

    async def retrieve(self, blob_id: str) -> bytes:
        try:
            result = await self.db_session.get(BlobData, blob_id)
            if result is None:
                raise BlobNotFoundError(f"Blob {blob_id} not found")
            return result.data
        except BlobNotFoundError:
            raise
        except Exception as e:
            raise StorageBackendError(f"Failed to retrieve blob: {str(e)}") from e

    async def exists(self, blob_id: str) -> bool:
        try:
            result = await self.db_session.get(BlobData, blob_id)
            return result is not None
        except Exception as e:
            raise StorageBackendError(f"Failed to check blob existence: {str(e)}") from e

    async def delete(self, blob_id: str) -> None:
        try:
            result = await self.db_session.get(BlobData, blob_id)
            if result:
                await self.db_session.delete(result)
                await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise StorageBackendError(f"Failed to delete blob: {str(e)}") from e

