"""API v1 routes."""

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas import BlobCreateRequest, BlobCreateResponse, BlobResponse

router = APIRouter(prefix="/v1", tags=["blobs"])


@router.post("/blobs", response_model=BlobCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_blob(request: BlobCreateRequest):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented",
    )


@router.get("/blobs/{blob_id}", response_model=BlobResponse)
async def get_blob(blob_id: str):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented",
    )
