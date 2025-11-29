# PR 5: API Foundation

## Description
Implements API schemas, routes skeleton, and router registration.

## Changes
- Pydantic models for requests and responses
- POST and GET endpoints for blob operations
- Router integrated with main FastAPI app
- Separate response schemas for POST (no data) and GET (with data)

## Files Changed
- `app/api/v1/schemas.py`
- `app/api/v1/router.py`
- `app/main.py`

## Commits
- `df329e2` - Add API request and response schemas
- `b8f892a` - Add API routes skeleton
- `9bc4f49` - Register API v1 router
- `873a351` - Update API schemas to match specification

## Related
- Sprint 1 Task 1.3: API Schemas
- Sprint 1 Task 1.4: API Routes Skeleton

