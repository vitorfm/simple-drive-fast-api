# Sprint 2 - Storage Backends & API Integration

**Duration**: Week 2  
**Goal**: Implement storage backend abstraction, core storage backends, blob service, and integrate with API endpoints

---

## Sprint Overview

This sprint focuses on implementing the storage backend abstraction layer and two core storage backends (Local Filesystem and Database). We'll also create the blob service to orchestrate storage operations and integrate everything with the API endpoints. Authentication will be implemented to secure the API.

---

## Tasks for Senior Software Engineer

### Task 2.1: Storage Backend Abstraction Interface
**Priority**: High  
**Estimated Time**: 3-4 hours (Implementation: 2h, Tests: 1-2h)

**Description:**
Create the abstract base class that defines the interface all storage backends must implement.

**Requirements:**
- Create `StorageBackend` abstract base class in `app/storage/base.py`
- Define abstract methods:
  - `async def store(blob_id: str, data: bytes) -> None`
  - `async def retrieve(blob_id: str) -> bytes`
  - `async def delete(blob_id: str) -> None` (optional, can raise NotImplementedError)
  - `async def exists(blob_id: str) -> bool`
- Add proper type hints and docstrings
- Define custom exceptions for storage operations

**Acceptance Criteria:**
- [ ] Abstract base class defined with all required methods
- [ ] Type hints and docstrings complete
- [ ] Cannot instantiate abstract class directly
- [ ] Interface is clear and well-documented

**Testing Requirements:**
- [ ] Test that abstract class cannot be instantiated
- [ ] Test that subclasses must implement all abstract methods
- [ ] Test exception handling structure

**Files to Create/Modify:**
- `app/storage/base.py`
- `tests/unit/test_storage_base.py`

---

### Task 2.2: Local Filesystem Storage Backend
**Priority**: High  
**Estimated Time**: 5-6 hours (Implementation: 3-4h, Tests: 2h)

**Description:**
Implement the local filesystem storage backend that stores blobs as files on disk.

**Requirements:**
- Implement `LocalStorageBackend` class inheriting from `StorageBackend`
- Store files in configurable directory (`LOCAL_STORAGE_PATH`)
- Sanitize blob IDs for filesystem safety (handle special characters, path traversal)
- Optional: Use subdirectory hashing (e.g., first 2 chars of ID) to avoid too many files in one directory
- Handle file creation, reading, deletion, and existence checks
- Proper error handling for filesystem operations (permissions, disk full, etc.)
- Async file operations using `aiofiles` library

**Implementation Details:**
- Sanitize blob ID: Remove/replace invalid filesystem characters
- File naming: Use sanitized blob ID as filename
- Directory structure: `{LOCAL_STORAGE_PATH}/{sanitized_id}` or `{LOCAL_STORAGE_PATH}/{prefix}/{sanitized_id}`
- Create storage directory if it doesn't exist
- Handle concurrent access (file locking if needed)

**Acceptance Criteria:**
- [ ] Can store blobs to local filesystem
- [ ] Can retrieve blobs from local filesystem
- [ ] Can check if blob exists
- [ ] Can delete blobs (optional)
- [ ] Handles invalid blob IDs (sanitization)
- [ ] Handles filesystem errors gracefully
- [ ] Storage directory created automatically if missing

**Testing Requirements:**
- [ ] Test storing blob data
- [ ] Test retrieving stored blob
- [ ] Test retrieving non-existent blob (raises error)
- [ ] Test exists() method (true/false)
- [ ] Test delete() method
- [ ] Test blob ID sanitization
- [ ] Test concurrent access scenarios
- [ ] Test error handling (permissions, disk full, etc.)
- [ ] Test with various blob sizes (small, medium, large)
- [ ] Use temporary directories for testing

**Files to Create/Modify:**
- `app/storage/local.py`
- `tests/unit/test_storage_local.py`
- `requirements.txt` (add `aiofiles`)

---

### Task 2.3: Database Storage Backend
**Priority**: High  
**Estimated Time**: 5-6 hours (Implementation: 3-4h, Tests: 2h)

**Description:**
Implement the database storage backend that stores blob data in a separate database table.

**Requirements:**
- Create new SQLAlchemy model `BlobData` for storing actual blob data
  - `id` (PRIMARY KEY, String)
  - `data` (BYTEA/BLOB, LargeBinary)
  - `created_at` (DateTime, UTC)
- Create Alembic migration for `blob_data` table
- Implement `DatabaseStorageBackend` class
- Use async SQLAlchemy operations
- Handle database errors appropriately
- Support both SQLite and PostgreSQL

**Implementation Details:**
- Table name: `blob_data`
- Separate from `blob_metadata` table (data vs metadata separation)
- Use SQLAlchemy `LargeBinary` type for blob data
- Handle large blobs efficiently (streaming if needed)
- Transaction management for consistency

**Acceptance Criteria:**
- [ ] `blob_data` table created via migration
- [ ] Can store blob data in database
- [ ] Can retrieve blob data from database
- [ ] Can check if blob exists in database
- [ ] Can delete blob from database
- [ ] Handles database errors gracefully
- [ ] Works with both SQLite and PostgreSQL

**Testing Requirements:**
- [ ] Test storing blob data
- [ ] Test retrieving stored blob
- [ ] Test retrieving non-existent blob (raises error)
- [ ] Test exists() method
- [ ] Test delete() method
- [ ] Test with various blob sizes
- [ ] Test database error handling
- [ ] Test transaction rollback on errors
- [ ] Use test database (in-memory SQLite)

**Files to Create/Modify:**
- `app/models/blob_data.py`
- `app/storage/database.py`
- `alembic/versions/002_add_blob_data_table.py`
- `tests/unit/test_storage_database.py`

---

### Task 2.4: Storage Backend Factory
**Priority**: High  
**Estimated Time**: 2-3 hours (Implementation: 1-2h, Tests: 1h)

**Description:**
Create a factory function that instantiates the correct storage backend based on configuration.

**Requirements:**
- Create factory function `get_storage_backend()` in `app/storage/__init__.py`
- Read `STORAGE_BACKEND` from configuration
- Return appropriate backend instance:
  - `"local"` → `LocalStorageBackend`
  - `"database"` → `DatabaseStorageBackend`
  - `"s3"` → Raise error (not implemented yet)
  - `"ftp"` → Raise error (not implemented yet)
- Pass required configuration to backend constructors
- Handle invalid storage backend configuration

**Acceptance Criteria:**
- [ ] Factory returns correct backend based on config
- [ ] Backend is properly initialized with config
- [ ] Invalid backend name raises clear error
- [ ] Factory is a singleton or cached (same instance returned)

**Testing Requirements:**
- [ ] Test factory returns LocalStorageBackend for "local"
- [ ] Test factory returns DatabaseStorageBackend for "database"
- [ ] Test factory raises error for invalid backend name
- [ ] Test factory raises error for unimplemented backends
- [ ] Test backend initialization with config values

**Files to Create/Modify:**
- `app/storage/__init__.py`
- `tests/unit/test_storage_factory.py`

---

### Task 2.5: Blob Service Layer
**Priority**: High  
**Estimated Time**: 4-5 hours (Implementation: 2-3h, Tests: 2h)

**Description:**
Create the blob service that orchestrates storage operations and metadata management.

**Requirements:**
- Create `BlobService` class in `app/services/blob_service.py`
- Methods:
  - `async def create_blob(blob_id: str, data: bytes) -> BlobMetadata`
  - `async def get_blob(blob_id: str) -> tuple[bytes, BlobMetadata]`
  - `async def blob_exists(blob_id: str) -> bool`
- Service responsibilities:
  - Validate blob ID doesn't already exist (for create)
  - Store data using storage backend
  - Create/update metadata in database
  - Retrieve data and metadata together
  - Handle errors and rollback if needed
- Use dependency injection for storage backend and database session

**Implementation Details:**
- Check metadata table first to see if blob exists
- Store data in selected storage backend
- Create metadata record with: id, size, created_at, storage_backend, storage_path
- For retrieval: get metadata first, then retrieve data from backend
- Handle case where metadata exists but data doesn't (inconsistency)
- Use database transactions for consistency

**Acceptance Criteria:**
- [ ] Can create blob (stores data + metadata)
- [ ] Can retrieve blob (returns data + metadata)
- [ ] Prevents duplicate blob IDs
- [ ] Handles missing blobs gracefully
- [ ] Metadata and data stay in sync
- [ ] Proper error handling and rollback

**Testing Requirements:**
- [ ] Test creating new blob
- [ ] Test creating duplicate blob ID (raises error)
- [ ] Test retrieving existing blob
- [ ] Test retrieving non-existent blob (raises error)
- [ ] Test blob_exists() method
- [ ] Test metadata creation with correct values
- [ ] Test error handling and rollback
- [ ] Test with different storage backends (local, database)
- [ ] Mock storage backend for unit tests

**Files to Create/Modify:**
- `app/services/blob_service.py`
- `tests/unit/test_blob_service.py`

---

### Task 2.6: API Endpoint Integration
**Priority**: High  
**Estimated Time**: 3-4 hours (Implementation: 2h, Tests: 1-2h)

**Description:**
Integrate the blob service with API endpoints to make them fully functional.

**Requirements:**
- Update `POST /v1/blobs` endpoint:
  - Validate Base64 data
  - Decode Base64 to bytes
  - Call blob service to create blob
  - Return proper response with id, size, created_at
  - Handle errors (invalid Base64, duplicate ID, etc.)
- Update `GET /v1/blobs/{id}` endpoint:
  - Call blob service to retrieve blob
  - Encode data back to Base64
  - Return response with id, data, size, created_at
  - Handle errors (not found, etc.)
- Use FastAPI dependency injection for blob service
- Proper HTTP status codes (201, 200, 400, 404, 409)

**Acceptance Criteria:**
- [ ] POST endpoint stores blobs successfully
- [ ] POST endpoint validates Base64
- [ ] POST endpoint prevents duplicates
- [ ] GET endpoint retrieves blobs successfully
- [ ] GET endpoint returns correct response format
- [ ] GET endpoint handles missing blobs (404)
- [ ] All error cases return appropriate status codes
- [ ] Response schemas match specification

**Testing Requirements:**
- [ ] Integration test: POST with valid data
- [ ] Integration test: POST with invalid Base64
- [ ] Integration test: POST with duplicate ID
- [ ] Integration test: GET existing blob
- [ ] Integration test: GET non-existent blob
- [ ] Test response schemas match specification
- [ ] Test HTTP status codes
- [ ] Test with both storage backends
- [ ] End-to-end test: store and retrieve

**Files to Create/Modify:**
- `app/api/v1/router.py`
- `app/api/v1/dependencies.py` (service dependency)
- `tests/integration/test_api_endpoints.py`

---

### Task 2.7: Authentication Implementation
**Priority**: High  
**Estimated Time**: 3-4 hours (Implementation: 2h, Tests: 1-2h)

**Description:**
Implement Bearer token authentication to secure API endpoints.

**Requirements:**
- Create authentication dependency in `app/dependencies.py`
- Function: `async def verify_token(authorization: Header) -> str`
- Extract Bearer token from Authorization header
- Validate token against configured `API_TOKEN`
- Raise 401 if token missing or invalid
- Apply authentication to all blob endpoints
- Simple implementation: compare with env var token

**Implementation Details:**
- Header format: `Authorization: Bearer <token>`
- Token stored in `API_TOKEN` environment variable
- Case-sensitive token comparison
- Clear error messages for missing/invalid tokens

**Acceptance Criteria:**
- [ ] All endpoints require authentication
- [ ] Valid token allows access
- [ ] Missing token returns 401
- [ ] Invalid token returns 401
- [ ] Error messages are clear

**Testing Requirements:**
- [ ] Test endpoint with valid token (success)
- [ ] Test endpoint without Authorization header (401)
- [ ] Test endpoint with invalid token (401)
- [ ] Test endpoint with malformed header (401)
- [ ] Test all endpoints are protected
- [ ] Integration test: full flow with auth

**Files to Create/Modify:**
- `app/dependencies.py`
- `app/api/v1/router.py` (add auth dependency)
- `tests/unit/test_auth.py`
- `tests/integration/test_auth_integration.py`

---

## Sprint Deliverables

By the end of Sprint 2, we should have:

1. ✅ Storage backend abstraction interface
2. ✅ Local filesystem storage backend (fully functional)
3. ✅ Database storage backend (fully functional)
4. ✅ Storage backend factory
5. ✅ Blob service layer
6. ✅ Fully functional API endpoints (POST and GET)
7. ✅ Authentication protecting all endpoints
8. ✅ Comprehensive test coverage for all components

---

## Dependencies

- **Task 2.1** (Abstraction) → Required for Tasks 2.2, 2.3
- **Task 2.2** (Local) → Required for Task 2.4
- **Task 2.3** (Database) → Required for Task 2.4
- **Task 2.4** (Factory) → Required for Task 2.5
- **Task 2.5** (Service) → Required for Task 2.6
- **Task 2.7** (Auth) → Can be done in parallel, but needed before Task 2.6 completion

---

## Testing Strategy

### Unit Tests
- Test each storage backend in isolation
- Test blob service with mocked storage backends
- Test authentication logic
- Test factory function

### Integration Tests
- Test API endpoints end-to-end
- Test with real storage backends
- Test authentication flow
- Test error scenarios

### Test Coverage Goals
- Aim for >80% code coverage
- All critical paths tested
- Edge cases covered
- Error handling tested

---

## Definition of Done

A task is considered complete when:
- [ ] Code implemented and working
- [ ] All tests written and passing
- [ ] Code follows project style (black formatting)
- [ ] Type hints added where appropriate
- [ ] Docstrings added for public methods
- [ ] No linter errors
- [ ] Acceptance criteria met
- [ ] Integration tested with other components

---

## Additional Notes

### Storage Backend Selection
- Start with `local` backend for development
- Test with `database` backend
- Both should work interchangeably

### Error Handling
- Use custom exceptions from `app/utils/exceptions.py`
- Provide clear error messages
- Log errors appropriately

### Performance Considerations
- Local storage: Consider file system limits
- Database storage: Consider blob size limits (PostgreSQL BYTEA can handle large data)
- Async operations throughout for better performance

### Security
- Sanitize blob IDs for filesystem safety
- Validate all inputs
- Authentication on all endpoints
- Consider rate limiting (future)

---

## Next Sprint Preview

Sprint 3 will focus on:
- S3-compatible storage backend (HTTP-only implementation)
- AWS Signature Version 4 implementation
- S3 integration testing
- Optional: FTP storage backend (bonus)

---

**Sprint Start Date**: [To be filled]  
**Sprint End Date**: [To be filled]  
**Sprint Review Date**: [To be filled]

