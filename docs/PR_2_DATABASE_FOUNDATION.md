# PR 2: Database Foundation

## Description
Sets up the complete database infrastructure including SQLAlchemy async support, BlobMetadata model, Alembic migrations, and database session management. This enables metadata storage separate from blob data storage.

## Changes
- **Database Connection**: Async SQLAlchemy engine and session management
- **BlobMetadata Model**: SQLAlchemy model with all required fields (id, size, created_at, storage_backend, storage_path)
- **Alembic Setup**: Complete migration system configured for async operations
- **Initial Migration**: Creates `blob_metadata` table with proper schema

## Files Changed
- `app/database.py` - Database connection and session management
- `app/models/blob_metadata.py` - BlobMetadata SQLAlchemy model
- `app/config.py` - Added debug field for database echo
- `requirements.txt` - Added aiosqlite dependency
- `alembic.ini` - Alembic configuration
- `alembic/env.py` - Alembic environment setup with async support
- `alembic/script.py.mako` - Migration template
- `alembic/versions/001_initial_migration.py` - Initial migration

## Commits
- Add aiosqlite dependency for async SQLite support
- Add database connection and session management
- Create BlobMetadata database model
- Set up Alembic for database migrations
- Create initial database migration

## Related
- Sprint 1 Task 1.1: Database Setup & Metadata Model
- Part of Phase 1: Foundation

## Testing
- [ ] Database connection works (SQLite for dev)
- [ ] Alembic migrations can be run (`alembic upgrade head`)
- [ ] `blob_metadata` table created with correct schema
- [ ] Model can be imported and used in FastAPI app

## Database Schema
```sql
CREATE TABLE blob_metadata (
    id VARCHAR(255) PRIMARY KEY,
    size INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    storage_backend VARCHAR(50) NOT NULL,
    storage_path VARCHAR(512)
);
```

