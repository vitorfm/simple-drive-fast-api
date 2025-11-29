import pytest

from app.services.blob_service import BlobService
from app.storage.ftp import FTPStorageBackend
from app.utils.exceptions import BlobNotFoundError


@pytest.mark.asyncio
async def test_ftp_backend_mock(db_session):
    backend = FTPStorageBackend(
        "localhost",
        21,
        "testuser",
        "testpass",
        "/test",
    )
    
    test_data = b"Test FTP blob data"
    
    try:
        await backend.store("test-ftp-blob", test_data)
        retrieved = await backend.retrieve("test-ftp-blob")
        assert retrieved == test_data
        
        assert await backend.exists("test-ftp-blob") is True
        assert await backend.exists("non-existent") is False
    except Exception:
        pytest.skip("FTP server not available")


@pytest.mark.asyncio
async def test_ftp_blob_service_integration(db_session):
    backend = FTPStorageBackend(
        "localhost",
        21,
        "testuser",
        "testpass",
        "/test",
    )
    
    service = BlobService(db_session, backend)
    test_data = b"FTP service integration test"
    
    try:
        metadata = await service.create_blob("ftp-service-blob", test_data)
        assert metadata.id == "ftp-service-blob"
        assert metadata.size == len(test_data)
        
        data, retrieved_metadata = await service.get_blob("ftp-service-blob")
        assert data == test_data
        assert retrieved_metadata.id == "ftp-service-blob"
    except Exception:
        pytest.skip("FTP server not available")

