from datetime import datetime

from pydantic import BaseModel, Field


class BlobCreateRequest(BaseModel):
    id: str = Field(..., description="Blob identifier")
    data: str = Field(..., description="Base64 encoded data")


class BlobCreateResponse(BaseModel):
    id: str
    size: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class BlobResponse(BaseModel):
    id: str
    data: str
    size: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }
