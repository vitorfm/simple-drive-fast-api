import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.storage.ftp import FTPStorageBackend
from app.utils.exceptions import BlobNotFoundError, StorageBackendError


@pytest.fixture
def mock_ftp_client():
    client = AsyncMock()
    client.list = AsyncMock(return_value=[])
    client.upload_stream = AsyncMock()
    client.download_stream = AsyncMock()
    client.remove_file = AsyncMock()
    client.change_directory = AsyncMock()
    client.make_directory = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_ftp_store_success(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        
        mock_stream = AsyncMock()
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_ftp_client.upload_stream = AsyncMock(return_value=mock_context)
        
        await backend.store("test-blob", b"test data")
        
        mock_ftp_client.upload_stream.assert_called_once()
        mock_stream.write.assert_called_once_with(b"test data")


@pytest.mark.asyncio
async def test_ftp_retrieve_success(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        
        file_info = MagicMock()
        file_info.name = "test-blob"
        mock_ftp_client.list.return_value = [file_info]
        
        mock_stream = AsyncMock()
        mock_stream.read = AsyncMock(side_effect=[b"test ", b"data", b""])
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_ftp_client.download_stream = AsyncMock(return_value=mock_context)
        
        result = await backend.retrieve("test-blob")
        
        assert result == b"test data"
        mock_ftp_client.download_stream.assert_called_once()


@pytest.mark.asyncio
async def test_ftp_retrieve_not_found(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        mock_ftp_client.list.return_value = []
        
        with pytest.raises(BlobNotFoundError):
            await backend.retrieve("non-existent")


@pytest.mark.asyncio
async def test_ftp_exists_true(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        
        file_info = MagicMock()
        file_info.name = "test-blob"
        mock_ftp_client.list.return_value = [file_info]
        
        result = await backend.exists("test-blob")
        assert result is True


@pytest.mark.asyncio
async def test_ftp_exists_false(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        mock_ftp_client.list.return_value = []
        
        result = await backend.exists("non-existent")
        assert result is False


@pytest.mark.asyncio
async def test_ftp_delete_success(mock_ftp_client):
    backend = FTPStorageBackend("localhost", 21, "user", "pass", "/base")
    
    with patch("aioftp.Client", return_value=mock_ftp_client):
        backend.client = mock_ftp_client
        
        await backend.delete("test-blob")
        
        mock_ftp_client.remove_file.assert_called_once()


@pytest.mark.asyncio
async def test_ftp_connection_error():
    backend = FTPStorageBackend("invalid-host", 21, "user", "pass")
    
    with patch("aioftp.Client") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock(side_effect=Exception("Connection failed"))
        mock_client_class.return_value = mock_client
        
        with pytest.raises(StorageBackendError, match="Failed to connect"):
            await backend.store("test", b"data")

