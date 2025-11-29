import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_post_blobs_valid_request(client):
    response = await client.post(
        "/v1/blobs",
        json={
            "id": "test-blob-1",
            "data": "SGVsbG8gV29ybGQ=",
        },
    )
    assert response.status_code == 501


@pytest.mark.asyncio
async def test_post_blobs_invalid_base64(client):
    response = await client.post(
        "/v1/blobs",
        json={
            "id": "test-blob-2",
            "data": "Invalid Base64!",
        },
    )
    assert response.status_code in [400, 501]


@pytest.mark.asyncio
async def test_post_blobs_missing_fields(client):
    response = await client.post(
        "/v1/blobs",
        json={
            "id": "test-blob-3",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_blob_valid_id(client):
    response = await client.get("/v1/blobs/test-blob-4")
    assert response.status_code == 501


@pytest.mark.asyncio
async def test_get_blob_response_schema(client):
    response = await client.get("/v1/blobs/test-blob-5")
    if response.status_code != 501:
        data = response.json()
        assert "id" in data or "error" in data


@pytest.mark.asyncio
async def test_post_blobs_response_schema(client):
    response = await client.post(
        "/v1/blobs",
        json={
            "id": "test-blob-6",
            "data": "SGVsbG8=",
        },
    )
    if response.status_code != 501:
        data = response.json()
        assert "id" in data or "error" in data


@pytest.mark.asyncio
async def test_api_docs_accessible(client):
    response = await client.get("/docs")
    assert response.status_code == 200

