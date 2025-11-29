# Simple Drive

FastAPI application for storing and retrieving binary data (blobs) with multiple storage backends.

## Features

- Store and retrieve blobs via REST API
- Multiple storage backends: Local Filesystem, Database, S3-compatible, FTP
- Bearer token authentication
- Base64-encoded data support

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Configuration

Set environment variables or create `.env` file:

```bash
STORAGE_BACKEND=local  # Options: local, database, s3, ftp
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
LOCAL_STORAGE_PATH=./storage
```

## API Endpoints

- `POST /v1/blobs` - Store a blob
- `GET /v1/blobs/{id}` - Retrieve a blob

All endpoints require Bearer token authentication.

## Storage Backends

- **Local**: Filesystem storage
- **Database**: SQLAlchemy blob storage
- **S3**: S3-compatible storage (HTTP-only, no SDK)
- **FTP**: FTP server storage

## Testing

```bash
pytest tests/ -v
```

## Documentation

See [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for detailed project plan.

