from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.blob_metadata import BlobMetadata
from app.storage.base import StorageBackend
from app.utils.exceptions import BlobAlreadyExistsError, BlobNotFoundError


class BlobService:
    def __init__(self, storage_backend: StorageBackend, db_session: AsyncSession):
        self.storage_backend = storage_backend
        self.db_session = db_session

    async def create_blob(self, blob_id: str, data: bytes) -> BlobMetadata:
        existing = await self.db_session.get(BlobMetadata, blob_id)
        if existing:
            raise BlobAlreadyExistsError(f"Blob {blob_id} already exists")

        await self.storage_backend.store(blob_id, data)

        metadata = BlobMetadata(
            id=blob_id,
            size=len(data),
            created_at=datetime.now(timezone.utc),
            storage_backend=self.storage_backend.__class__.__name__.replace("StorageBackend", "").lower(),
            storage_path=blob_id,
        )
        self.db_session.add(metadata)
        await self.db_session.commit()
        return metadata

    async def get_blob(self, blob_id: str) -> tuple[bytes, BlobMetadata]:
        metadata = await self.db_session.get(BlobMetadata, blob_id)
        if not metadata:
            raise BlobNotFoundError(f"Blob {blob_id} not found")

        data = await self.storage_backend.retrieve(blob_id)
        return data, metadata

    async def blob_exists(self, blob_id: str) -> bool:
        metadata = await self.db_session.get(BlobMetadata, blob_id)
        if metadata:
            return True
        return await self.storage_backend.exists(blob_id)

