# How to Create Pull Requests

## PR 1: Project Structure Setup

**Branch**: `feature/project-structure`  
**Base**: `master`

### Steps:
1. Visit: https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/project-structure
2. Or go to: Repository → Pull requests → New pull request
3. Select `feature/project-structure` as the source branch
4. Use the title and description below

### PR Title:
```
feat: Project structure setup
```

### PR Description:
```markdown
## Description
Creates the complete project directory structure with all necessary `__init__.py` files for the application modules. This establishes the foundation for the layered architecture as defined in the project plan.

## Changes
- Created directory structure for all application modules:
  - `app/api/v1/` - API version 1 routes
  - `app/services/` - Business logic layer
  - `app/storage/` - Storage backend implementations
  - `app/models/` - Database models
  - `app/utils/` - Utility functions
  - `tests/unit/` - Unit tests
  - `tests/integration/` - Integration tests
- Added all required `__init__.py` files to make modules importable

## Files Changed
- `app/api/__init__.py`
- `app/api/v1/__init__.py`
- `app/services/__init__.py`
- `app/storage/__init__.py`
- `app/models/__init__.py`
- `app/utils/__init__.py`
- `tests/__init__.py`
- `tests/unit/__init__.py`
- `tests/integration/__init__.py`

## Related
- Sprint 1 Task 1.1 (implicit - structure setup)
- Part of Phase 1: Foundation

## Testing
- No functional changes, structure only
- Verify all directories exist and are importable
```

---

## PR 2: Database Foundation

**Branch**: `feature/database-foundation`  
**Base**: `master` (or `feature/project-structure` if PR 1 is merged)

### Steps:
1. First push the branch: `git push origin feature/database-foundation`
2. Visit: https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/database-foundation
3. Use the title and description from `docs/PR_2_DATABASE_FOUNDATION.md`

### PR Title:
```
feat: Database foundation setup
```

---

## PR 3: Utilities & Exceptions

**Branch**: `feature/utilities-exceptions`  
**Base**: `master` (or previous PRs if merged)

### Steps:
1. First push the branch: `git push origin feature/utilities-exceptions`
2. Visit: https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/utilities-exceptions
3. Use the title and description from `docs/PR_3_UTILITIES_EXCEPTIONS.md`

### PR Title:
```
feat: Add utilities and custom exceptions
```

---

## PR 4: Configuration Management

**Branch**: `feature/configuration`  
**Base**: `master` (or previous PRs if merged)

### Steps:
1. First push the branch: `git push origin feature/configuration`
2. Visit: https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/configuration
3. Use the title and description from `docs/PR_4_CONFIGURATION.md`

### PR Title:
```
feat: Enhanced configuration management
```

---

## Quick Commands

To push all branches at once:
```bash
git push origin feature/project-structure
git push origin feature/database-foundation
git push origin feature/utilities-exceptions
git push origin feature/configuration
```

To open PR creation pages:
```bash
# PR 1
open "https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/project-structure"

# PR 2
open "https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/database-foundation"

# PR 3
open "https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/utilities-exceptions"

# PR 4
open "https://github.com/vitorfm/simple-drive-fast-api/pull/new/feature/configuration"
```

