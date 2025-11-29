from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.v1.router import router
from app.utils.exceptions import (
    BlobAlreadyExistsError,
    BlobNotFoundError,
    InvalidBase64Error,
    SimpleDriveError,
    StorageBackendError,
)

app = FastAPI(title="Simple Drive", version="1.0.0")
app.include_router(router)


@app.exception_handler(InvalidBase64Error)
async def invalid_base64_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid Base64 encoding", "detail": str(exc)},
    )


@app.exception_handler(BlobNotFoundError)
async def blob_not_found_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Blob not found", "detail": str(exc)},
    )


@app.exception_handler(BlobAlreadyExistsError)
async def blob_already_exists_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "Blob already exists", "detail": str(exc)},
    )


@app.exception_handler(StorageBackendError)
async def storage_backend_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Storage backend error", "detail": str(exc)},
    )


@app.exception_handler(SimpleDriveError)
async def simple_drive_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal error", "detail": str(exc)},
    )


@app.get("/")
def root():
    return {"message": "Simple Drive API"}

