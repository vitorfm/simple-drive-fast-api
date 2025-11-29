import pytest
from datetime import datetime, timezone

from app.models.blob_metadata import BlobMetadata


@pytest.mark.asyncio
async def test_model_creation_with_all_fields(db_session):
    blob = BlobMetadata(
        id="test-id-1",
        size=100,
        created_at=datetime.now(timezone.utc),
        storage_backend="local",
        storage_path="/path/to/blob",
    )
    db_session.add(blob)
    await db_session.commit()
    
    result = await db_session.get(BlobMetadata, "test-id-1")
    assert result.id == "test-id-1"
    assert result.size == 100
    assert result.storage_backend == "local"
    assert result.storage_path == "/path/to/blob"
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_model_creation_with_optional_fields(db_session):
    blob = BlobMetadata(
        id="test-id-2",
        size=200,
        created_at=datetime.now(timezone.utc),
        storage_backend="database",
    )
    db_session.add(blob)
    await db_session.commit()
    
    result = await db_session.get(BlobMetadata, "test-id-2")
    assert result.id == "test-id-2"
    assert result.size == 200
    assert result.storage_backend == "database"
    assert result.storage_path is None


@pytest.mark.asyncio
async def test_timestamp_auto_generation(db_session):
    blob = BlobMetadata(
        id="test-id-3",
        size=300,
        storage_backend="s3",
    )
    db_session.add(blob)
    await db_session.commit()
    
    result = await db_session.get(BlobMetadata, "test-id-3")
    assert result.created_at is not None
    assert result.created_at.tzinfo == timezone.utc


@pytest.mark.asyncio
async def test_unique_id_constraint(db_session):
    blob1 = BlobMetadata(
        id="duplicate-id",
        size=100,
        storage_backend="local",
    )
    blob2 = BlobMetadata(
        id="duplicate-id",
        size=200,
        storage_backend="local",
    )
    
    db_session.add(blob1)
    await db_session.commit()
    
    db_session.add(blob2)
    with pytest.raises(Exception):
        await db_session.commit()

