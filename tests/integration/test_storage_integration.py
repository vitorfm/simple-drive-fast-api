import pytest
import base64

from app.services.blob_service import BlobService
from app.storage.database import DatabaseStorageBackend
from app.storage.local import LocalStorageBackend
from app.utils.exceptions import BlobNotFoundError, BlobAlreadyExistsError


@pytest.mark.asyncio
async def test_local_storage_store_and_retrieve(db_session, tmp_path):
    backend = LocalStorageBackend(str(tmp_path))
    test_data = b"Hello World"
    
    await backend.store("test-blob-1", test_data)
    retrieved = await backend.retrieve("test-blob-1")
    
    assert retrieved == test_data
    assert await backend.exists("test-blob-1") is True
    assert await backend.exists("non-existent") is False


@pytest.mark.asyncio
async def test_database_storage_store_and_retrieve(db_session):
    backend = DatabaseStorageBackend(db_session)
    test_data = b"Hello Database"
    
    await backend.store("test-blob-2", test_data)
    retrieved = await backend.retrieve("test-blob-2")
    
    assert retrieved == test_data
    assert await backend.exists("test-blob-2") is True


@pytest.mark.asyncio
async def test_blob_service_create_and_get_local(db_session, tmp_path):
    backend = LocalStorageBackend(str(tmp_path))
    service = BlobService(backend, db_session)
    
    test_data = b"Test blob data"
    metadata = await service.create_blob("service-blob-1", test_data)
    
    assert metadata.id == "service-blob-1"
    assert metadata.size == len(test_data)
    
    data, retrieved_metadata = await service.get_blob("service-blob-1")
    assert data == test_data
    assert retrieved_metadata.id == "service-blob-1"


@pytest.mark.asyncio
async def test_blob_service_duplicate_id(db_session, tmp_path):
    backend = LocalStorageBackend(str(tmp_path))
    service = BlobService(backend, db_session)
    
    await service.create_blob("duplicate-test", b"data")
    
    with pytest.raises(BlobAlreadyExistsError):
        await service.create_blob("duplicate-test", b"other data")


@pytest.mark.asyncio
async def test_blob_service_not_found(db_session, tmp_path):
    backend = LocalStorageBackend(str(tmp_path))
    service = BlobService(backend, db_session)
    
    with pytest.raises(BlobNotFoundError):
        await service.get_blob("non-existent-blob")

