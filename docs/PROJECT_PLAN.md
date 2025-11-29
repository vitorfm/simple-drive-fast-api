# Simple Drive - FastAPI Project Plan

## Executive Summary

This document outlines the implementation plan for **Simple Drive**, a FastAPI-based object storage service that provides a unified interface for multiple storage backends. The project demonstrates software engineering principles including object-oriented design, abstraction, and clean architecture.

## Project Overview

### Objectives
- Build a RESTful API for storing and retrieving binary data (blobs)
- Implement a pluggable storage backend architecture
- Support multiple storage backends: S3-compatible, Database, Local Filesystem, and FTP
- Implement authentication and authorization
- Maintain separation between metadata and data storage

### Key Requirements
- **API Endpoints**: POST /v1/blobs, GET /v1/blobs/{id}
- **Storage Backends**: S3-compatible (HTTP-only), Database, Local FS, FTP (bonus)
- **Authentication**: Bearer token authentication
- **Metadata Tracking**: Separate database table for blob metadata
- **Testing**: Unit and integration tests (bonus points)

---

## Architecture & Design

### High-Level Architecture

```
┌─────────────────┐
│   FastAPI App   │
│   (API Layer)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Auth Layer     │
│  (Dependencies) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Service Layer   │
│  (Business Logic)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│Storage │ │   Metadata   │
│Backend │ │   Database   │
│Abst.   │ │   (ORM)      │
└───┬────┘ └──────────────┘
    │
    ├──► S3-Compatible (HTTP)
    ├──► Database Table
    ├──► Local Filesystem
    └──► FTP Server
```

### Design Principles

1. **Abstraction Layer**: Storage backends implement a common interface
2. **Separation of Concerns**: API, Business Logic, Storage, and Metadata are separate layers
3. **Dependency Injection**: Storage backend selected via configuration
4. **Single Responsibility**: Each component has one clear purpose

---

## Technical Stack

### Core Framework
- **FastAPI**: Modern Python web framework
- **Python 3.9+**: Language version

### Database & ORM
- **SQLAlchemy**: ORM for metadata storage
- **Alembic**: Database migrations
- **PostgreSQL/SQLite**: Database options (configurable)

### HTTP Client
- **httpx**: Async HTTP client for S3-compatible storage
- **requests**: Alternative sync client (if needed)

### Authentication
- **python-jose**: JWT token handling (simple implementation)
- **passlib**: Password hashing (if needed for token generation)

### FTP
- **ftplib**: Standard library FTP client

### Testing
- **pytest**: Testing framework
- **httpx**: Test client for FastAPI
- **pytest-asyncio**: Async test support
- **pytest-mock**: Mocking utilities

### Development Tools
- **black**: Code formatting
- **flake8/mypy**: Linting and type checking
- **pre-commit**: Git hooks

---

## Project Structure

```
simple-drive-fast-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── dependencies.py          # FastAPI dependencies (auth)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # API route definitions
│   │       └── schemas.py      # Pydantic models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── blob_service.py     # Business logic for blobs
│   │   └── auth_service.py     # Authentication logic
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract base class
│   │   ├── s3_compatible.py    # S3 via HTTP
│   │   ├── database.py         # Database storage
│   │   ├── local.py             # Local filesystem
│   │   └── ftp.py               # FTP storage (bonus)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── blob_metadata.py    # SQLAlchemy models
│   │
│   └── utils/
│       ├── __init__.py
│       ├── base64_validator.py # Base64 validation
│       └── exceptions.py       # Custom exceptions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/
│   │   ├── test_base64.py
│   │   ├── test_storage_backends.py
│   │   └── test_auth.py
│   └── integration/
│       ├── test_api_contract.py
│       └── test_storage_integration.py
│
├── alembic/                    # Database migrations
│   └── versions/
│
├── docs/
│   └── PROJECT_PLAN.md         # This document
│
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml              # Project config (black, mypy, etc.)
└── README.md
```

---

## API Specifications

### POST /v1/blobs

**Request:**
```json
{
  "id": "any_valid_string_or_identifier",
  "data": "SGVsbG8gU2ltcGxlIFN0b3JhZ2UgV29ybGQh"
}
```

**Response (201 Created):**
```json
{
  "id": "any_valid_string_or_identifier",
  "size": 27,
  "created_at": "2023-01-22T21:37:55Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid Base64 encoding
- `401 Unauthorized`: Missing or invalid token
- `409 Conflict`: Blob ID already exists

### GET /v1/blobs/{id}

**Response (200 OK):**
```json
{
  "id": "any_valid_string_or_identifier",
  "data": "SGVsbG8gU2ltcGxlIFN0b3JhZ2UgV29ybGQh",
  "size": 27,
  "created_at": "2023-01-22T21:37:55Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: Blob not found

---

## Storage Backend Abstraction

### Base Interface

```python
class StorageBackend(ABC):
    @abstractmethod
    async def store(self, blob_id: str, data: bytes) -> None:
        """Store binary data with given ID"""
        pass
    
    @abstractmethod
    async def retrieve(self, blob_id: str) -> bytes:
        """Retrieve binary data by ID"""
        pass
    
    @abstractmethod
    async def delete(self, blob_id: str) -> None:
        """Delete blob by ID (optional)"""
        pass
    
    @abstractmethod
    async def exists(self, blob_id: str) -> bool:
        """Check if blob exists"""
        pass
```

### Implementation Details

#### 1. S3-Compatible Storage (`s3_compatible.py`)
- **Protocol**: HTTP-based S3 API
- **Libraries**: `httpx` only (no boto3 or similar)
- **Key Operations**:
  - PUT object: `PUT /{bucket}/{key}`
  - GET object: `GET /{bucket}/{key}`
  - HEAD object: `HEAD /{bucket}/{key}` (for exists check)
- **Authentication**: AWS Signature Version 4 (implement manually)
- **Configuration**:
  - Endpoint URL
  - Access Key ID
  - Secret Access Key
  - Bucket name

#### 2. Database Storage (`database.py`)
- **Table Design**: Separate table for blob data
  - `id` (PRIMARY KEY)
  - `data` (BYTEA/BLOB)
  - `created_at` (TIMESTAMP)
- **ORM**: SQLAlchemy
- **Configuration**: Database connection string

#### 3. Local Filesystem Storage (`local.py`)
- **Directory Structure**: Configurable base path
- **Naming Convention**: Use blob ID as filename (with sanitization)
- **Subdirectory Strategy**: Optional subdirectory hashing (e.g., first 2 chars of ID)
- **Configuration**: Storage directory path

#### 4. FTP Storage (`ftp.py`) - Bonus
- **Library**: `ftplib` (standard library)
- **Operations**: STOR, RETR, LIST
- **Configuration**:
  - FTP host
  - Port
  - Username
  - Password
  - Base directory

---

## Database Schema

### Blob Metadata Table

```sql
CREATE TABLE blob_metadata (
    id VARCHAR(255) PRIMARY KEY,
    size INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    storage_backend VARCHAR(50) NOT NULL,
    storage_path VARCHAR(512),  -- Optional: path/key in storage backend
    INDEX idx_created_at (created_at),
    INDEX idx_storage_backend (storage_backend)
);
```

**Notes:**
- `id`: Unique identifier (matches blob ID)
- `size`: Size in bytes
- `created_at`: ISO8601 UTC timestamp
- `storage_backend`: Which backend stored this (e.g., 's3', 'database', 'local', 'ftp')
- `storage_path`: Optional path/key within the backend

---

## Authentication Strategy

### Simple Bearer Token Implementation

**Approach:**
1. Generate simple API tokens (UUID or random string)
2. Store tokens in database or environment variable
3. Validate token via FastAPI dependency

**Token Storage Options:**
- **Option A**: Environment variable (simple, single token)
- **Option B**: Database table (multiple tokens, user management)
- **Option C**: JWT tokens (more complex, but scalable)

**Recommended**: Start with Option A (env var), design for Option B (database)

**FastAPI Dependency:**
```python
async def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    # Validate token
    if not is_valid_token(token):
        raise HTTPException(401, "Invalid token")
    return token
```

---

## Configuration Management

### Environment Variables

```bash
# Application
APP_ENV=development
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost/simpledrive
# or
DATABASE_URL=sqlite:///./simpledrive.db

# Storage Backend Selection
STORAGE_BACKEND=s3  # Options: s3, database, local, ftp

# S3-Compatible Storage
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=simpledrive-bucket
S3_REGION=us-east-1

# Local Filesystem Storage
LOCAL_STORAGE_PATH=/home/john/server_storage

# FTP Storage
FTP_HOST=ftp.example.com
FTP_PORT=21
FTP_USERNAME=user
FTP_PASSWORD=pass
FTP_BASE_DIR=/storage

# Authentication
API_TOKEN=your-secret-token-here
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal**: Core infrastructure and API skeleton

**Tasks:**
- [ ] Project structure setup
- [ ] FastAPI app initialization
- [ ] Configuration management
- [ ] Database setup (SQLAlchemy + Alembic)
- [ ] Metadata model and migrations
- [ ] Basic API routes (skeleton)
- [ ] Base64 validation utility
- [ ] Error handling and custom exceptions

**Deliverables:**
- Working FastAPI app (no storage yet)
- Database migrations
- API contract defined (Pydantic schemas)

### Phase 2: Storage Abstraction (Week 1-2)
**Goal**: Implement storage backend interface and core backends

**Tasks:**
- [ ] Define `StorageBackend` abstract base class
- [ ] Implement Local Filesystem backend
- [ ] Implement Database backend
- [ ] Storage backend factory/selector
- [ ] Integration with blob service

**Deliverables:**
- Working storage abstraction
- At least 2 backends functional (local, database)

### Phase 3: S3-Compatible Storage (Week 2)
**Goal**: Implement S3-compatible storage using HTTP only

**Tasks:**
- [ ] Research S3 API protocol
- [ ] Implement AWS Signature Version 4
- [ ] Implement PUT operation (store)
- [ ] Implement GET operation (retrieve)
- [ ] Implement HEAD operation (exists check)
- [ ] Error handling for S3 responses
- [ ] Configuration and testing

**Deliverables:**
- Fully functional S3-compatible backend
- Documentation of S3 protocol implementation

### Phase 4: Authentication (Week 2)
**Goal**: Implement Bearer token authentication

**Tasks:**
- [ ] Token validation logic
- [ ] FastAPI dependency for auth
- [ ] Apply auth to all endpoints
- [ ] Error responses for unauthorized requests
- [ ] Token management (simple implementation)

**Deliverables:**
- Protected API endpoints
- Authentication working end-to-end

### Phase 5: FTP Storage (Week 3) - Bonus
**Goal**: Implement FTP storage backend

**Tasks:**
- [ ] FTP connection management
- [ ] Implement store operation
- [ ] Implement retrieve operation
- [ ] Implement exists check
- [ ] Error handling
- [ ] Configuration

**Deliverables:**
- Functional FTP backend
- Integrated with storage abstraction

### Phase 6: Testing (Week 3)
**Goal**: Comprehensive test coverage

**Tasks:**
- [ ] Unit tests for Base64 validation
- [ ] Unit tests for each storage backend
- [ ] Unit tests for authentication
- [ ] Integration tests for API contract
- [ ] Integration tests for storage backends
- [ ] Test fixtures and mocks
- [ ] CI/CD test configuration

**Deliverables:**
- Test suite with >80% coverage
- All tests passing

### Phase 7: Documentation & Polish (Week 3-4)
**Goal**: Finalize project documentation and code quality

**Tasks:**
- [ ] README with setup instructions
- [ ] API documentation (FastAPI auto-docs)
- [ ] Code comments and docstrings
- [ ] Code formatting (black)
- [ ] Type hints (mypy)
- [ ] Linting (flake8)
- [ ] Performance testing
- [ ] Security review

**Deliverables:**
- Complete documentation
- Production-ready code

---

## Testing Strategy

### Unit Tests

**Coverage Areas:**
1. **Base64 Validation**
   - Valid Base64 strings
   - Invalid Base64 strings
   - Edge cases (empty, special characters)

2. **Storage Backends**
   - Each backend implementation
   - Store operation
   - Retrieve operation
   - Exists check
   - Error handling

3. **Authentication**
   - Valid token validation
   - Invalid token rejection
   - Missing token handling

4. **Service Layer**
   - Blob service logic
   - Metadata creation
   - Error propagation

### Integration Tests

**Coverage Areas:**
1. **API Contract**
   - POST /v1/blobs (success and error cases)
   - GET /v1/blobs/{id} (success and error cases)
   - Request/response schema validation
   - Status codes

2. **Storage Integration**
   - End-to-end flow with each backend
   - Data integrity verification
   - Concurrent access (if applicable)

3. **Authentication Integration**
   - Protected endpoints with valid token
   - Protected endpoints with invalid token
   - Protected endpoints without token

### Test Structure

```python
# Example test structure
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_base64_validator.py
│   ├── test_storage_local.py
│   ├── test_storage_database.py
│   ├── test_storage_s3.py
│   ├── test_storage_ftp.py
│   ├── test_auth.py
│   └── test_blob_service.py
└── integration/
    ├── test_api_blobs.py
    ├── test_storage_backends.py
    └── test_auth_flow.py
```

---

## Risk Assessment & Mitigation

### Technical Risks

1. **S3 Protocol Complexity**
   - **Risk**: AWS Signature V4 is complex to implement
   - **Mitigation**: Start with research, use test S3-compatible service (MinIO) for development

2. **Storage Backend Switching**
   - **Risk**: Data migration when switching backends
   - **Mitigation**: Design abstraction carefully, document migration process

3. **Concurrent Access**
   - **Risk**: Race conditions with blob IDs
   - **Mitigation**: Database constraints, proper transaction handling

4. **Large File Handling**
   - **Risk**: Memory issues with large blobs
   - **Mitigation**: Stream data where possible, set size limits

### Project Risks

1. **Timeline**
   - **Risk**: S3 implementation may take longer
   - **Mitigation**: Prioritize core backends first, S3 can be refined

2. **Testing Coverage**
   - **Risk**: Insufficient test coverage
   - **Mitigation**: Write tests alongside implementation, not after

---

## Success Criteria

### Functional Requirements
- ✅ POST /v1/blobs stores data successfully
- ✅ GET /v1/blobs/{id} retrieves data correctly
- ✅ Base64 validation works properly
- ✅ All 4 storage backends functional
- ✅ Authentication protects all endpoints
- ✅ Metadata stored separately from data

### Non-Functional Requirements
- ✅ Clean, maintainable code structure
- ✅ Comprehensive test coverage (>80%)
- ✅ Proper error handling
- ✅ Configuration management
- ✅ Documentation complete

### Bonus Points
- ✅ FTP backend implemented
- ✅ Comprehensive test suite
- ✅ Code quality tools (linting, formatting)

---

## Dependencies

### Production Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
httpx>=0.25.0
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.6
```

### Development Dependencies
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-mock>=3.12.0
httpx>=0.25.0
black>=23.10.0
flake8>=6.1.0
mypy>=1.6.0
pre-commit>=3.5.0
```

---

## Next Steps

1. **Review this plan** with the team
2. **Assign tasks** based on expertise:
   - Senior Engineer: S3 implementation, architecture decisions
   - QA Engineer: Test strategy, test implementation
3. **Set up development environment**
4. **Begin Phase 1** implementation
5. **Schedule regular sync meetings** (daily standups recommended)

---

## Questions for Discussion

1. **Database Choice**: PostgreSQL vs SQLite for development/production?
2. **Token Management**: Simple env var vs database table?
3. **File Size Limits**: Should we impose maximum blob size?
4. **Concurrency**: How to handle concurrent requests for same blob ID?
5. **Deployment**: Target deployment environment (Docker, cloud, etc.)?

---

## Appendix: S3 Protocol Research Notes

### Key S3 Operations (HTTP-based)

1. **PUT Object**
   - Method: `PUT`
   - URL: `https://{endpoint}/{bucket}/{key}`
   - Headers: Authorization (AWS Signature), Content-Length, Content-Type
   - Body: Binary data

2. **GET Object**
   - Method: `GET`
   - URL: `https://{endpoint}/{bucket}/{key}`
   - Headers: Authorization (AWS Signature)

3. **HEAD Object**
   - Method: `HEAD`
   - URL: `https://{endpoint}/{bucket}/{key}`
   - Headers: Authorization (AWS Signature)
   - Response: Metadata without body

### AWS Signature Version 4
- Requires: Access Key ID, Secret Access Key, Region, Service name
- Steps: Create canonical request → String to sign → Signature
- Reference: AWS documentation for Signature Version 4

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Engineering Team  
**Status**: Draft for Review

