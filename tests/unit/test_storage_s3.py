import pytest
from unittest.mock import AsyncMock, patch

from app.storage.s3_compatible import S3CompatibleStorageBackend
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


@pytest.mark.asyncio
async def test_s3_store_success():
    backend = S3CompatibleStorageBackend(
        "https://s3.amazonaws.com",
        "test-bucket",
        "access-key",
        "secret-key",
    )
    
    with patch.object(backend.client, "put", new_callable=AsyncMock) as mock_put:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        await backend.store("test-blob", b"test data")
        
        mock_put.assert_called_once()
        assert "Authorization" in mock_put.call_args[1]["headers"]


@pytest.mark.asyncio
async def test_s3_retrieve_success():
    backend = S3CompatibleStorageBackend(
        "https://s3.amazonaws.com",
        "test-bucket",
        "access-key",
        "secret-key",
    )
    
    with patch.object(backend.client, "get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.content = b"test data"
        mock_get.return_value = mock_response
        
        result = await backend.retrieve("test-blob")
        
        assert result == b"test data"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_s3_retrieve_not_found():
    backend = S3CompatibleStorageBackend(
        "https://s3.amazonaws.com",
        "test-bucket",
        "access-key",
        "secret-key",
    )
    
    with patch.object(backend.client, "get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with pytest.raises(BlobNotFoundError):
            await backend.retrieve("non-existent")


@pytest.mark.asyncio
async def test_s3_exists_true():
    backend = S3CompatibleStorageBackend(
        "https://s3.amazonaws.com",
        "test-bucket",
        "access-key",
        "secret-key",
    )
    
    with patch.object(backend.client, "head", new_callable=AsyncMock) as mock_head:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        result = await backend.exists("test-blob")
        
        assert result is True


@pytest.mark.asyncio
async def test_s3_exists_false():
    backend = S3CompatibleStorageBackend(
        "https://s3.amazonaws.com",
        "test-bucket",
        "access-key",
        "secret-key",
    )
    
    with patch.object(backend.client, "head", new_callable=AsyncMock) as mock_head:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response
        
        result = await backend.exists("non-existent")
        
        assert result is False

