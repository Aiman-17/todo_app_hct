---
id: 0005
title: Session Management and Test Fixes
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5
feature: 002-fullstack-web-auth
branch: 002-fullstack-web-auth
user: ACS
command: direct-prompt
labels: ["session-management", "token-refresh", "draft-preservation", "testing", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/auth.py
  - backend/src/schemas/auth.py
  - backend/src/services/auth_service.py
  - backend/tests/conftest.py
  - backend/tests/integration/test_auth_api.py
  - backend/tests/unit/test_services.py
  - frontend/src/lib/api.ts
  - frontend/src/components/tasks/TaskForm.tsx
  - specs/002-fullstack-web-auth/tasks-phase2-ui-enhancements.md
tests:
  - backend/tests/integration/test_auth_api.py::test_signup_success
  - backend/tests/integration/test_auth_api.py::test_signup_duplicate_email
  - backend/tests/integration/test_auth_api.py::test_signup_invalid_password
  - backend/tests/integration/test_auth_api.py::test_login_success
  - backend/tests/integration/test_auth_api.py::test_login_invalid_credentials
  - backend/tests/integration/test_auth_api.py::test_get_profile_authenticated
  - backend/tests/integration/test_auth_api.py::test_get_profile_unauthenticated
  - backend/tests/unit/test_services.py::test_hash_password
  - backend/tests/unit/test_services.py::test_verify_password
  - backend/tests/unit/test_services.py::test_create_access_token
  - backend/tests/unit/test_services.py::test_create_refresh_token
  - backend/tests/unit/test_services.py::test_verify_token
  - backend/tests/unit/test_services.py::test_verify_token_invalid
  - backend/tests/unit/test_services.py::test_verify_token_expired
---

## Prompt

User requested three main improvements:

1. **Session Management**: "change user story session never expired if user loguot for longtime because this will lost user work"
   - Implement automatic token refresh to prevent session expiration
   - Add draft preservation to prevent work loss

2. **Test Fixes**: "fix integration test and also fix json error if user delete task 'failed to delete task unexpected end of json input'"
   - Fix 13 failing integration tests (out of 41 total)
   - Fix JSON parse error on task deletion

3. **Error Messages**: "pleaset log developer level error messages to user because this will confused user"
   - Remove technical error messages that confuse end users
   - Provide user-friendly error messages

4. **UI Enhancement Tasks**: User requested comprehensive tasks file for Phase 2 UI enhancements with premium minimalist design (Rose White #FFF0EB, Seal Brown #2D0B00), icon-first interactions, priorities, tags, recurring tasks, due dates, notifications, multi-language support (including Urdu), and voice commands.

## Response snapshot

### 1. Session Management Implementation

**Backend Token Refresh Endpoint** (`backend/src/api/auth.py:189-283`):
- Added `/api/auth/refresh` POST endpoint
- Validates refresh token type (prevents access tokens from being used)
- Returns new access + refresh token pair
- Handles expired tokens with user-friendly error messages

**Extended Token Lifetimes**:
- Access token: 15 minutes → 1 hour (3600 seconds)
- Refresh token: 7 days → 30 days
- Updated in `auth_service.py`, `auth.py` schemas, and `api.ts`

**Frontend Automatic Refresh** (`frontend/src/lib/api.ts:105-140`):
- Modified `apiRequest()` to detect 401 token expiration errors
- Automatically calls `refreshAccessToken()` on expiration
- Retries original request with new token (once only, prevents loops)
- Redirects to login only if refresh fails

**Draft Preservation** (`frontend/src/components/tasks/TaskForm.tsx:35-89`):
- Auto-saves title and description to localStorage on every change
- Loads draft on component mount
- Shows "Draft saved" indicator
- Clears draft after successful task creation

### 2. Test Fixes

**Integration Test Database Override** (`backend/tests/conftest.py:16,81,89`):
- Fixed dependency injection: changed from `get_session` to `get_db_session`
- Tests now properly use in-memory SQLite instead of production database
- Result: 41/41 tests passing (100%)

**Token Expiration Test Updates**:
- `test_auth_api.py`: Updated `expires_in` assertions from 900 to 3600 seconds
- `test_services.py`: Updated access token test from 14-16 min to 59-61 min
- `test_services.py`: Updated refresh token test from ~7 days to ~30 days

### 3. JSON Deletion Error Fix

**Root Cause**: DELETE endpoint returns 204 No Content (empty body), but frontend tried to parse as JSON

**Fix** (`frontend/src/lib/api.ts:97-109`):
```typescript
if (response.status === 204) {
  data = null;  // No body to parse
} else {
  // Parse JSON normally
}
```

### 4. User-Friendly Error Messages

**Added SyntaxError Handler** (`frontend/src/lib/api.ts:170-176`):
```typescript
if (error instanceof SyntaxError) {
  throw new APIError(
    'Something went wrong. Please try again.',  // User-friendly
    0,
    null
  );
}
```

### 5. UI Enhancement Tasks File

**Created**: `specs/002-fullstack-web-auth/tasks-phase2-ui-enhancements.md`
- 138 tasks organized into 21 phases
- Design system with custom colors (#FFF0EB, #2D0B00)
- Icon-first interactions with lucide-react
- Card-based layout with soft shadows and animations
- Advanced features: priorities, tags, recurring tasks, due dates, notifications
- Responsive design (mobile/tablet/desktop)
- Accessibility (keyboard navigation, ARIA labels, screen readers)
- Bonus: Multi-language support (Urdu RTL), voice commands
- MVP scope: Phases 1-9 (68 tasks)
- 60% parallelization (83 tasks marked [P])

## Outcome

- ✅ Impact: Session management prevents work loss, automatic token refresh provides seamless UX, all tests passing, user-friendly error messages, comprehensive UI enhancement roadmap created
- 🧪 Tests: 41/41 passing (100% pass rate)
- 📁 Files: 9 files modified/created (5 backend, 2 frontend, 1 test config, 1 tasks file)
- 🔁 Next prompts: Begin implementing Phase 1 of UI enhancements (Design Foundation), or deploy session management improvements
- 🧠 Reflection: Token refresh pattern is industry standard, localStorage draft preservation is simple but effective, fixing test database isolation was critical for test reliability

## Evaluation notes (flywheel)

- Failure modes observed: Initial test failures due to wrong dependency override, JSON parse errors on empty 204 responses, confusing technical error messages shown to users
- Graders run and results (PASS/FAIL): All 41 backend tests PASS (14 unit, 27 integration)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding service worker for offline draft persistence, or implementing periodic token refresh before expiration (proactive vs reactive)
