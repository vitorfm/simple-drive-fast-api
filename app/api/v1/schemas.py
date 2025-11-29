"""API request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class BlobCreateRequest(BaseModel):
    """Request schema for creating a blob."""

    id: str = Field(..., min_length=1)
    data: str = Field(..., description="Base64 encoded data")


class BlobResponse(BaseModel):
    """Response schema for blob data."""

    id: str
    data: str
    size: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }

