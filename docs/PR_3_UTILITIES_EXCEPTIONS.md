# PR 3: Utilities & Exceptions

## Description
Implements custom exception classes and Base64 validation utility with proper error handling. These utilities will be used throughout the application for consistent error handling and data validation.

## Changes
- **Custom Exceptions**: Base exception class and specific exceptions for different error scenarios
- **Base64 Validation**: Utility functions to validate and decode Base64 strings with proper error handling

## Files Changed
- `app/utils/exceptions.py` - Custom exception classes:
  - `SimpleDriveError` - Base exception
  - `InvalidBase64Error` - Invalid Base64 encoding
  - `BlobNotFoundError` - Blob not found
  - `BlobAlreadyExistsError` - Duplicate blob ID
  - `StorageBackendError` - Storage operation failure
- `app/utils/base64_validator.py` - Base64 validation and decoding:
  - `validate_base64()` - Validates Base64 string format
  - `decode_base64()` - Decodes Base64 to bytes

## Commits
- Add custom exception classes
- Implement Base64 validation utility

## Related
- Sprint 1 Task 1.2: Base64 Validation Utility
- Sprint 1 Task 1.6: Error Handling & Custom Exceptions (partial)
- Part of Phase 1: Foundation

## Testing
- [ ] Valid Base64 strings decode successfully
- [ ] Invalid Base64 strings raise `InvalidBase64Error`
- [ ] Empty strings handled appropriately
- [ ] Error messages are descriptive

## Usage Example
```python
from app.utils.base64_validator import decode_base64
from app.utils.exceptions import InvalidBase64Error

try:
    data = decode_base64("SGVsbG8gV29ybGQ=")
except InvalidBase64Error as e:
    # Handle error
    pass
```

