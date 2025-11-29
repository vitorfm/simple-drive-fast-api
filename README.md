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

Set environment variables or create `.env` file. Examples for each storage backend:

### Local Filesystem Storage

```bash
STORAGE_BACKEND=local
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
LOCAL_STORAGE_PATH=./storage
```

### Database Storage

```bash
STORAGE_BACKEND=database
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
```

For PostgreSQL:
```bash
STORAGE_BACKEND=database
DATABASE_URL=postgresql://user:password@localhost/simpledrive
API_TOKEN=your-secret-token
```

### S3-Compatible Storage

```bash
STORAGE_BACKEND=s3
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=simpledrive
S3_REGION=us-east-1
```

For AWS S3:
```bash
STORAGE_BACKEND=s3
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_ACCESS_KEY_ID=your_aws_access_key
S3_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET_NAME=your-bucket-name
S3_REGION=us-east-1
```

### FTP Storage

```bash
STORAGE_BACKEND=ftp
DATABASE_URL=sqlite:///./simpledrive.db
API_TOKEN=your-secret-token
FTP_HOST=localhost
FTP_PORT=21
FTP_USERNAME=ftpuser
FTP_PASSWORD=ftppass
FTP_BASE_DIR=/
```

**Note:** The `DATABASE_URL` is always required for metadata storage, regardless of the storage backend selected.

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

