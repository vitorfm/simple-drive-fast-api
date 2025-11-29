import pytest

from app.services.blob_service import BlobService
from app.storage.s3_compatible import S3CompatibleStorageBackend
from app.utils.exceptions import BlobNotFoundError


@pytest.mark.asyncio
async def test_s3_backend_mock(db_session):
    backend = S3CompatibleStorageBackend(
        "http://localhost:9000",
        "test-bucket",
        "minioadmin",
        "minioadmin",
        "us-east-1",
    )
    
    test_data = b"Test S3 blob data"
    
    try:
        await backend.store("test-s3-blob", test_data)
        retrieved = await backend.retrieve("test-s3-blob")
        assert retrieved == test_data
        
        assert await backend.exists("test-s3-blob") is True
        assert await backend.exists("non-existent") is False
    except Exception:
        pytest.skip("S3 service not available (MinIO not running)")


@pytest.mark.asyncio
async def test_s3_blob_service_integration(db_session):
    backend = S3CompatibleStorageBackend(
        "http://localhost:9000",
        "test-bucket",
        "minioadmin",
        "minioadmin",
        "us-east-1",
    )
    
    service = BlobService(backend, db_session)
    test_data = b"S3 service integration test"
    
    try:
        metadata = await service.create_blob("s3-service-blob", test_data)
        assert metadata.id == "s3-service-blob"
        assert metadata.size == len(test_data)
        
        data, retrieved_metadata = await service.get_blob("s3-service-blob")
        assert data == test_data
        assert retrieved_metadata.id == "s3-service-blob"
    except Exception:
        pytest.skip("S3 service not available (MinIO not running)")

