"""API v1 routes."""

import base64

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import BlobCreateRequest, BlobResponse
from app.database import get_db
from app.services.blob_service import BlobService
from app.storage import get_storage_backend
from app.utils.base64_validator import decode_base64
from app.utils.exceptions import BlobAlreadyExistsError, BlobNotFoundError, InvalidBase64Error

router = APIRouter(prefix="/v1", tags=["blobs"])


@router.post("/blobs", response_model=BlobResponse, status_code=status.HTTP_201_CREATED)
async def create_blob(
    request: BlobCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new blob."""
    try:
        data = decode_base64(request.data)
    except InvalidBase64Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    try:
        storage_backend = await get_storage_backend(db)
        blob_service = BlobService(storage_backend, db)
        metadata = await blob_service.create_blob(request.id, data)

        encoded_data = base64.b64encode(data).decode("utf-8")
        return BlobResponse(
            id=metadata.id,
            data=encoded_data,
            size=metadata.size,
            created_at=metadata.created_at,
        )
    except BlobAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get("/blobs/{blob_id}", response_model=BlobResponse)
async def get_blob(
    blob_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a blob by ID."""
    try:
        storage_backend = await get_storage_backend(db)
        blob_service = BlobService(storage_backend, db)
        data, metadata = await blob_service.get_blob(blob_id)

        encoded_data = base64.b64encode(data).decode("utf-8")
        return BlobResponse(
            id=metadata.id,
            data=encoded_data,
            size=metadata.size,
            created_at=metadata.created_at,
        )
    except BlobNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
