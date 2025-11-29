# Sprint 1 - Foundation & Infrastructure

**Duration**: Week 1  
**Goal**: Establish core infrastructure, database setup, and API skeleton

---

## Sprint Overview

This sprint focuses on setting up the foundational infrastructure for the Simple Drive project. We'll establish the database, create the API structure, implement basic validation, and set up the development environment.

---

## Tasks for Senior Software Engineer

### Task 1.1: Database Setup & Metadata Model
**Priority**: High  
**Estimated Time**: 4-6 hours

**Description:**
Set up SQLAlchemy with Alembic for database migrations. Create the blob metadata model and initial migration.

**Requirements:**
- Configure SQLAlchemy with async support
- Set up Alembic for database migrations
- Create `BlobMetadata` model with fields:
  - `id` (String, Primary Key)
  - `size` (Integer)
  - `created_at` (DateTime, UTC)
  - `storage_backend` (String)
  - `storage_path` (String, optional)
- Create initial Alembic migration
- Support both SQLite (development) and PostgreSQL (production)

**Acceptance Criteria:**
- [ ] Database connection working (SQLite for dev)
- [ ] Alembic migrations can be run (`alembic upgrade head`)
- [ ] `blob_metadata` table created with correct schema
- [ ] Model can be imported and used in FastAPI app

**Files to Create/Modify:**
- `app/models/blob_metadata.py`
- `app/database.py` (database session management)
- `alembic/env.py`
- `alembic/versions/001_initial_migration.py`

---

### Task 1.2: Base64 Validation Utility
**Priority**: High  
**Estimated Time**: 2-3 hours

**Description:**
Create a utility module for Base64 validation and decoding with proper error handling.

**Requirements:**
- Function to validate Base64 string format
- Function to decode Base64 to bytes
- Raise appropriate exceptions for invalid Base64
- Handle edge cases (empty strings, padding issues, invalid characters)

**Acceptance Criteria:**
- [ ] Valid Base64 strings decode successfully
- [ ] Invalid Base64 strings raise clear exceptions
- [ ] Empty strings handled appropriately
- [ ] Error messages are descriptive

**Files to Create/Modify:**
- `app/utils/base64_validator.py`
- `app/utils/exceptions.py` (custom exceptions)

---

### Task 1.3: API Schemas (Pydantic Models)
**Priority**: High  
**Estimated Time**: 2-3 hours

**Description:**
Define Pydantic models for API request/response validation.

**Requirements:**
- `BlobCreateRequest`: id (string), data (Base64 string)
- `BlobResponse`: id, data (Base64), size (int), created_at (datetime)
- Proper validation and serialization
- ISO8601 format for timestamps

**Acceptance Criteria:**
- [ ] Request schema validates input correctly
- [ ] Response schema serializes data properly
- [ ] Timestamps in ISO8601 UTC format
- [ ] Type validation working

**Files to Create/Modify:**
- `app/api/v1/schemas.py`

---

### Task 1.4: API Routes Skeleton
**Priority**: High  
**Estimated Time**: 3-4 hours

**Description:**
Create FastAPI route structure for blob endpoints (without storage logic yet).

**Requirements:**
- `POST /v1/blobs` endpoint (returns 501 Not Implemented for now)
- `GET /v1/blobs/{id}` endpoint (returns 501 Not Implemented for now)
- Proper route organization
- API versioning structure
- Error handling middleware

**Acceptance Criteria:**
- [ ] Routes are accessible at `/v1/blobs`
- [ ] Request validation works (Pydantic)
- [ ] Proper HTTP status codes
- [ ] FastAPI auto-docs accessible at `/docs`

**Files to Create/Modify:**
- `app/api/v1/router.py`
- `app/main.py` (register router)

---

### Task 1.5: Configuration Management Enhancement
**Priority**: Medium  
**Estimated Time**: 2 hours

**Description:**
Enhance the configuration system to support all required settings.

**Requirements:**
- Add all storage backend configurations
- Environment variable support via `.env` file
- Validation of required settings per backend
- Default values for development

**Acceptance Criteria:**
- [ ] All config options available
- [ ] Environment variables load correctly
- [ ] Validation prevents invalid configurations
- [ ] `.env.example` file updated

**Files to Create/Modify:**
- `app/config.py`
- `.env.example`

---

### Task 1.6: Error Handling & Custom Exceptions
**Priority**: Medium  
**Estimated Time**: 2-3 hours

**Description:**
Implement comprehensive error handling with custom exceptions.

**Requirements:**
- Custom exception classes:
  - `InvalidBase64Error`
  - `BlobNotFoundError`
  - `BlobAlreadyExistsError`
  - `StorageBackendError`
- FastAPI exception handlers
- Consistent error response format
- Proper HTTP status codes

**Acceptance Criteria:**
- [ ] Custom exceptions defined
- [ ] Exception handlers registered
- [ ] Error responses follow consistent format
- [ ] Appropriate status codes returned

**Files to Create/Modify:**
- `app/utils/exceptions.py`
- `app/main.py` (exception handlers)

---

## Tasks for QA Engineer

### Task 1.7: Test Environment Setup
**Priority**: High  
**Estimated Time**: 2-3 hours

**Description:**
Set up testing infrastructure with pytest and test fixtures.

**Requirements:**
- Configure pytest with pytest-asyncio
- Create test database setup/teardown
- Create test client fixtures
- Set up test configuration
- Create test utilities and helpers

**Acceptance Criteria:**
- [ ] `pytest` runs successfully
- [ ] Test database isolated from dev database
- [ ] Test fixtures available for use
- [ ] Async tests supported

**Files to Create/Modify:**
- `tests/conftest.py`
- `tests/__init__.py`
- `pytest.ini` or `pyproject.toml` (pytest config)

---

### Task 1.8: Base64 Validation Tests
**Priority**: High  
**Estimated Time**: 3-4 hours

**Description:**
Write comprehensive unit tests for Base64 validation utility.

**Test Cases:**
- Valid Base64 strings (various lengths)
- Invalid Base64 strings (wrong characters, malformed)
- Empty strings
- Strings with/without padding
- Unicode/UTF-8 encoded data
- Binary data encoding/decoding

**Acceptance Criteria:**
- [ ] All test cases pass
- [ ] Edge cases covered
- [ ] Test coverage >90% for base64_validator module
- [ ] Tests are well-documented

**Files to Create/Modify:**
- `tests/unit/test_base64_validator.py`

---

### Task 1.9: API Contract Tests
**Priority**: High  
**Estimated Time**: 4-5 hours

**Description:**
Write integration tests for API endpoints to verify request/response contracts.

**Test Cases:**
- `POST /v1/blobs`:
  - Valid request structure
  - Invalid Base64 in request
  - Missing required fields
  - Response schema validation
- `GET /v1/blobs/{id}`:
  - Valid ID format
  - Non-existent ID
  - Response schema validation
- HTTP status codes verification
- Response format validation

**Acceptance Criteria:**
- [ ] All API contract tests pass
- [ ] Request validation tested
- [ ] Response schema validated
- [ ] Status codes verified
- [ ] Tests use TestClient from FastAPI

**Files to Create/Modify:**
- `tests/integration/test_api_contract.py`

---

### Task 1.10: Database Model Tests
**Priority**: Medium  
**Estimated Time**: 2-3 hours

**Description:**
Write tests for the BlobMetadata database model.

**Test Cases:**
- Model creation with all fields
- Model creation with optional fields
- Field validation
- Timestamp auto-generation
- Database constraints (unique ID, etc.)

**Acceptance Criteria:**
- [ ] Model tests pass
- [ ] Database operations work correctly
- [ ] Constraints enforced
- [ ] Timestamps in UTC

**Files to Create/Modify:**
- `tests/unit/test_models.py`

---

## Sprint Deliverables

By the end of Sprint 1, we should have:

1. ✅ Working database with metadata table
2. ✅ Base64 validation utility with tests
3. ✅ API endpoints structure (skeleton)
4. ✅ Request/response schemas defined
5. ✅ Comprehensive test suite foundation
6. ✅ Error handling framework
7. ✅ Configuration system ready for all backends

---

## Dependencies

- **Task 1.1** (Database) → Required for Task 1.10
- **Task 1.2** (Base64) → Required for Task 1.8 and future API implementation
- **Task 1.3** (Schemas) → Required for Task 1.4 and Task 1.9
- **Task 1.4** (Routes) → Required for Task 1.9
- **Task 1.7** (Test Setup) → Required for all QA tasks

---

## Definition of Done

A task is considered complete when:
- [ ] Code implemented and working
- [ ] Code reviewed (if applicable)
- [ ] Tests written and passing
- [ ] No linter errors
- [ ] Documentation updated (if needed)
- [ ] Acceptance criteria met

---

## Questions & Notes

- Database: Start with SQLite for simplicity, ensure PostgreSQL compatibility
- API: Endpoints return 501 until storage backends are implemented (Sprint 2)
- Testing: Aim for >80% coverage on new code
- Code Quality: Use black for formatting, mypy for type checking

---

## Next Sprint Preview

Sprint 2 will focus on:
- Storage backend abstraction layer
- Local filesystem storage implementation
- Database storage implementation
- Integration with API endpoints

---

**Sprint Start Date**: [To be filled]  
**Sprint End Date**: [To be filled]  
**Sprint Review Date**: [To be filled]

