# Sprint 3 - S3-Compatible Storage & FTP Backend

**Duration**: Week 3  
**Goal**: Implement S3-compatible storage backend using HTTP-only (no SDKs) and optional FTP storage backend

---

## Sprint Overview

This sprint focuses on implementing the S3-compatible storage backend using only HTTP clients (no boto3 or AWS SDK). This is the most complex backend as it requires implementing AWS Signature Version 4 manually. We'll also implement the FTP storage backend as a bonus feature.

---

## Tasks for Senior Software Engineer

### Task 3.1: S3 Protocol Research & Design
**Priority**: High  
**Estimated Time**: 2-3 hours (Research: 1-2h, Design: 1h)

**Description:**
Research the S3 REST API protocol and design the implementation approach. Document the key requirements and create a design document.

**Requirements:**
- Research S3 REST API documentation
- Understand AWS Signature Version 4 signing process
- Document S3 endpoint structure and request format
- Identify required headers and query parameters
- Plan error handling for S3 responses
- Document compatibility with S3-compatible services (MinIO, DigitalOcean Spaces, etc.)

**Deliverables:**
- Design document with S3 API structure
- List of required HTTP operations
- Signature Version 4 algorithm steps documented
- Error response format documented

**Acceptance Criteria:**
- [ ] S3 API protocol understood
- [ ] Signature Version 4 process documented
- [ ] Design document created
- [ ] Implementation approach clear

**Files to Create/Modify:**
- `docs/S3_IMPLEMENTATION_DESIGN.md` (optional, for reference)

---

### Task 3.2: AWS Signature Version 4 Implementation
**Priority**: High  
**Estimated Time**: 6-8 hours (Implementation: 4-5h, Tests: 2-3h)

**Description:**
Implement AWS Signature Version 4 signing algorithm for authenticating S3 requests. This is the core authentication mechanism for S3-compatible storage.

**Requirements:**
- Create utility module for AWS Signature Version 4
- Implement canonical request creation
- Implement string-to-sign generation
- Implement signature calculation (HMAC-SHA256)
- Handle date/time formatting (ISO8601, YYYYMMDD)
- Support different regions
- Handle query string parameters
- Handle request headers (canonical headers, signed headers)

**Implementation Details:**
- Function: `create_signature_v4(method, uri, headers, payload, access_key, secret_key, region, service='s3')`
- Steps:
  1. Create canonical request
  2. Create string to sign
  3. Calculate signature
  4. Create authorization header
- Use `hmac` and `hashlib` from Python standard library
- Handle URL encoding properly

**Acceptance Criteria:**
- [ ] Signature Version 4 algorithm implemented
- [ ] Can generate valid signatures for S3 requests
- [ ] Handles different HTTP methods (PUT, GET, HEAD)
- [ ] Handles different regions
- [ ] Properly encodes URLs and headers
- [ ] Works with S3-compatible services

**Testing Requirements:**
- [ ] Test signature generation with known test vectors
- [ ] Test with different HTTP methods
- [ ] Test with different regions
- [ ] Test URL encoding edge cases
- [ ] Test header canonicalization
- [ ] Test with MinIO (if available) or mock S3 service
- [ ] Unit tests for each step of the algorithm

**Files to Create/Modify:**
- `app/utils/aws_sigv4.py`
- `tests/unit/test_aws_sigv4.py`

---

### Task 3.3: S3-Compatible Storage Backend - Core Implementation
**Priority**: High  
**Estimated Time**: 5-6 hours (Implementation: 3-4h, Tests: 2h)

**Description:**
Implement the S3-compatible storage backend class that uses HTTP client to interact with S3-compatible services.

**Requirements:**
- Create `S3CompatibleStorageBackend` class in `app/storage/s3_compatible.py`
- Implement `store()` method using HTTP PUT
- Implement `retrieve()` method using HTTP GET
- Implement `exists()` method using HTTP HEAD
- Use `httpx` for async HTTP requests
- Integrate Signature Version 4 signing
- Handle S3-specific headers (Content-Type, Content-Length, etc.)
- Support configurable endpoint URL (for MinIO, DigitalOcean, etc.)

**Implementation Details:**
- Constructor parameters:
  - `endpoint_url` (e.g., `https://s3.amazonaws.com` or `http://localhost:9000` for MinIO)
  - `bucket_name`
  - `access_key_id`
  - `secret_access_key`
  - `region` (default: `us-east-1`)
- URL structure: `{endpoint_url}/{bucket_name}/{blob_id}`
- For path-style buckets: `{endpoint_url}/{bucket_name}/{blob_id}`
- For virtual-hosted-style: `{bucket_name}.{endpoint_url}/{blob_id}` (support both)
- Handle binary data properly
- Set appropriate Content-Type headers

**Acceptance Criteria:**
- [ ] Can store blobs to S3-compatible service
- [ ] Can retrieve blobs from S3-compatible service
- [ ] Can check if blob exists
- [ ] Handles S3 error responses properly
- [ ] Works with different S3-compatible endpoints
- [ ] Proper error messages for S3 errors

**Testing Requirements:**
- [ ] Test store operation
- [ ] Test retrieve operation
- [ ] Test exists operation
- [ ] Test error handling (404, 403, 500, etc.)
- [ ] Test with mock S3 server or MinIO
- [ ] Test with different endpoint URLs
- [ ] Test with large blobs
- [ ] Mock httpx responses for unit tests

**Files to Create/Modify:**
- `app/storage/s3_compatible.py`
- `tests/unit/test_storage_s3.py`
- `requirements.txt` (ensure `httpx` is included)

---

### Task 3.4: S3 Configuration & Factory Integration
**Priority**: High  
**Estimated Time**: 2-3 hours (Implementation: 1-2h, Tests: 1h)

**Description:**
Add S3 configuration to settings and integrate S3 backend into the storage factory.

**Requirements:**
- Add S3 configuration fields to `app/config.py`:
  - `s3_endpoint_url`
  - `s3_access_key_id`
  - `s3_secret_access_key`
  - `s3_bucket_name`
  - `s3_region`
- Update `.env.example` with S3 configuration
- Update storage factory to instantiate S3 backend when `STORAGE_BACKEND=s3`
- Validate S3 configuration (all required fields present)
- Handle missing S3 configuration gracefully

**Acceptance Criteria:**
- [ ] S3 configuration added to settings
- [ ] Factory can create S3 backend instance
- [ ] Configuration validation works
- [ ] Clear error messages for missing config
- [ ] Environment variables documented

**Testing Requirements:**
- [ ] Test factory creates S3 backend with valid config
- [ ] Test factory raises error with missing config
- [ ] Test configuration loading from environment
- [ ] Test default values (if any)

**Files to Create/Modify:**
- `app/config.py`
- `app/storage/__init__.py`
- `.env.example`
- `tests/unit/test_storage_factory.py` (update)

---

### Task 3.5: S3 Integration Testing
**Priority**: High  
**Estimated Time**: 3-4 hours

**Description:**
Create comprehensive integration tests for S3-compatible storage backend with real or mock S3 service.

**Requirements:**
- Integration tests with S3-compatible service (MinIO recommended for local testing)
- Test end-to-end flow: store → retrieve → exists
- Test error scenarios
- Test with different blob sizes
- Test concurrent operations
- Test with different S3-compatible services (if possible)
- Document how to set up test environment

**Testing Setup:**
- Option 1: Use MinIO for local testing (recommended)
- Option 2: Use mock S3 server
- Option 3: Use actual S3 (with test credentials, optional)

**Acceptance Criteria:**
- [ ] Integration tests pass with S3-compatible service
- [ ] All operations tested end-to-end
- [ ] Error scenarios covered
- [ ] Test setup documented
- [ ] Tests can run in CI/CD (with mock or MinIO)

**Testing Requirements:**
- [ ] Integration test: store and retrieve blob
- [ ] Integration test: check existence
- [ ] Integration test: handle non-existent blob
- [ ] Integration test: error handling
- [ ] Test documentation for setup

**Files to Create/Modify:**
- `tests/integration/test_s3_integration.py`
- `docs/TESTING_S3.md` (setup instructions)
- `tests/conftest.py` (S3 test fixtures if needed)

---

### Task 3.6: FTP Storage Backend (Bonus)
**Priority**: Medium (Bonus)  
**Estimated Time**: 4-5 hours (Implementation: 3h, Tests: 1-2h)

**Description:**
Implement FTP storage backend as a bonus feature. This demonstrates the flexibility of the storage abstraction.

**Requirements:**
- Create `FTPStorageBackend` class in `app/storage/ftp.py`
- Use Python's `ftplib` (standard library) or `aioftp` for async operations
- Implement `store()` using FTP STOR command
- Implement `retrieve()` using FTP RETR command
- Implement `exists()` using FTP LIST/NLST command
- Handle FTP connection management (connect, disconnect)
- Support passive and active modes
- Handle FTP errors appropriately

**Implementation Details:**
- Constructor parameters:
  - `host`
  - `port` (default: 21)
  - `username`
  - `password`
  - `base_dir` (optional base directory)
- Use `aioftp` for async operations (recommended) or `ftplib` with thread pool
- Handle binary transfer mode
- Create directories if needed
- Handle file paths properly

**Acceptance Criteria:**
- [ ] Can store blobs via FTP
- [ ] Can retrieve blobs via FTP
- [ ] Can check if blob exists
- [ ] Handles FTP connection errors
- [ ] Handles FTP authentication errors
- [ ] Works with different FTP servers

**Testing Requirements:**
- [ ] Test store operation
- [ ] Test retrieve operation
- [ ] Test exists operation
- [ ] Test error handling (connection, auth, etc.)
- [ ] Test with mock FTP server or real FTP server
- [ ] Integration tests if possible

**Files to Create/Modify:**
- `app/storage/ftp.py`
- `app/config.py` (add FTP config)
- `app/storage/__init__.py` (add FTP to factory)
- `tests/unit/test_storage_ftp.py`
- `requirements.txt` (add `aioftp` if using async)

---

### Task 3.7: FTP Configuration & Factory Integration
**Priority**: Medium (Bonus)  
**Estimated Time**: 1-2 hours

**Description:**
Add FTP configuration and integrate into storage factory.

**Requirements:**
- Add FTP configuration to `app/config.py`
- Update `.env.example`
- Update storage factory
- Validate FTP configuration

**Acceptance Criteria:**
- [ ] FTP configuration added
- [ ] Factory can create FTP backend
- [ ] Configuration validated

**Testing Requirements:**
- [ ] Test factory creates FTP backend
- [ ] Test configuration validation

**Files to Create/Modify:**
- `app/config.py`
- `app/storage/__init__.py`
- `.env.example`

---

## Sprint Deliverables

By the end of Sprint 3, we should have:

1. ✅ AWS Signature Version 4 implementation
2. ✅ S3-compatible storage backend (fully functional)
3. ✅ S3 integration tests
4. ✅ FTP storage backend (bonus, fully functional)
5. ✅ All storage backends integrated and working
6. ✅ Comprehensive test coverage

---

## Dependencies

- **Task 3.1** (Research) → Should be done first to inform implementation
- **Task 3.2** (Signature V4) → Required for Task 3.3
- **Task 3.3** (S3 Backend) → Required for Task 3.4 and Task 3.5
- **Task 3.4** (S3 Config) → Can be done in parallel with Task 3.3
- **Task 3.5** (S3 Tests) → Requires Task 3.3 and Task 3.4
- **Task 3.6** (FTP Backend) → Can be done independently
- **Task 3.7** (FTP Config) → Requires Task 3.6

---

## Testing Strategy

### Unit Tests
- AWS Signature Version 4 algorithm
- S3 backend operations (with mocked HTTP)
- FTP backend operations (with mocked FTP)

### Integration Tests
- S3 backend with real S3-compatible service (MinIO)
- FTP backend with real or mock FTP server
- End-to-end API tests with S3 backend
- End-to-end API tests with FTP backend

### Test Setup
- **MinIO**: Recommended for local S3 testing
  - Docker: `docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"`
  - Create test bucket and credentials
- **Mock FTP Server**: Use `pyftpdlib` or similar for testing
- **Real Services**: Optional, for final validation

---

## Resources & References

### AWS Signature Version 4
- [AWS Documentation: Signing AWS API Requests](https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html)
- [AWS Signature Version 4 Test Suite](https://docs.aws.amazon.com/general/latest/gr/signature-v4-test-suite.html)

### S3 REST API
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)
- [S3-Compatible Services](https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services)

### MinIO (Testing)
- [MinIO Documentation](https://min.io/docs/)
- [MinIO Python SDK](https://github.com/minio/minio-py) - For reference only, don't use

### FTP
- [Python ftplib Documentation](https://docs.python.org/3/library/ftplib.html)
- [aioftp Library](https://github.com/romlok/aioftp) - For async FTP

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
- [ ] Integration tested (where applicable)
- [ ] Documentation updated (if needed)

---

## Additional Notes

### S3 Implementation Challenges

1. **Signature Version 4 Complexity**
   - Multi-step algorithm with specific formatting requirements
   - Date/time handling is critical
   - URL encoding must be exact
   - Header canonicalization must match AWS exactly

2. **S3-Compatible Services**
   - Different services may have slight variations
   - Test with MinIO (most compatible)
   - Some services use path-style vs virtual-hosted-style URLs

3. **Error Handling**
   - S3 returns XML error responses
   - Parse XML to extract error codes and messages
   - Map S3 errors to application exceptions

### FTP Implementation Notes

1. **Async vs Sync**
   - `ftplib` is synchronous, may need thread pool
   - `aioftp` is async-native (recommended)
   - Consider performance implications

2. **Connection Management**
   - Reuse connections when possible
   - Handle connection timeouts
   - Handle network errors gracefully

3. **Security**
   - FTP is not secure by default
   - Consider FTPS (FTP over SSL) for production
   - Document security considerations

### Performance Considerations

- S3: Use connection pooling with httpx
- FTP: Reuse connections, handle timeouts
- Large blobs: Consider streaming for both backends
- Error retries: Implement retry logic for transient errors

---

## Next Steps After Sprint 3

After Sprint 3 completion:
- All storage backends implemented (local, database, S3, FTP)
- Project requirements fully met
- Optional: Performance optimization
- Optional: Additional features (blob deletion, listing, etc.)
- Optional: Production deployment preparation

---

**Sprint Start Date**: [To be filled]  
**Sprint End Date**: [To be filled]  
**Sprint Review Date**: [To be filled]

