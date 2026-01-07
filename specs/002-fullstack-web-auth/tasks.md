# Tasks: Phase II - Full-Stack Web Application with Authentication

**Input**: Design documents from `/specs/002-fullstack-web-auth/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (required), research.md (required), contracts/openapi.yaml (required)

**Tests**: Backend tests using pytest (unit tests for models/services, integration tests for API endpoints). Frontend manual testing (login/logout flows, CRUD operations, responsive design, error handling).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. MVP scope = User Story 1 + User Story 2 (P1 priorities).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- Paths shown assume web app structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for backend and frontend

- [X] T001 Create backend directory structure with subdirectories: backend/src/{models,schemas,services,api,middleware}, backend/tests/{unit,integration,contract}
- [X] T002 Initialize Python project in backend/ with pyproject.toml, requirements.txt (FastAPI, Uvicorn, SQLModel, psycopg2-binary, python-dotenv, bcrypt, pyjwt, pydantic[email])
- [X] T003 [P] Create frontend directory structure with Next.js 16+ App Router: frontend/src/{app,components,lib,types}, frontend/tests/{unit,integration}
- [X] T004 [P] Initialize Next.js TypeScript project in frontend/ with package.json (next ^15.1.0, react ^19.0.0, tailwindcss, shadcn/ui dependencies)
- [X] T005 [P] Create backend/.env.example template with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS placeholders
- [X] T006 [P] Create frontend/.env.local.example template with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET placeholders
- [X] T007 [P] Configure Tailwind CSS in frontend/tailwind.config.ts with shadcn/ui theme integration
- [X] T008 [P] Initialize shadcn/ui in frontend/ and install base components: button, input, card, dialog, form, label, toast using npx shadcn-ui@latest add
- [X] T009 Update root README.md with Phase II overview, setup instructions referencing specs/002-fullstack-web-auth/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create backend database configuration in backend/src/database.py with SQLModel engine, Neon connection pooling (pool_size=5, max_overflow=10, pool_pre_ping=True), session management, create_db_and_tables() function
- [X] T011 Create backend config module in backend/src/config.py to load environment variables (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS) using python-dotenv
- [X] T012 Create backend main application entry point in backend/src/main.py with FastAPI app initialization, CORS middleware (configure CORS_ORIGINS), startup event to call create_db_and_tables(), health check endpoint GET /api/health
- [X] T013 [P] Create backend User SQLModel in backend/src/models/user.py with fields (id UUID PK, email unique indexed, name, password_hash, created_at, updated_at), per data-model.md User schema
- [X] T014 [P] Create backend Task SQLModel in backend/src/models/task.py with fields (id int PK auto-increment, user_id UUID FK to users.id indexed, title max 200, description max 2000, completed default False, created_at, updated_at), per data-model.md Task schema with composite index (user_id, completed, created_at DESC)
- [X] T015 Create backend Pydantic auth schemas in backend/src/schemas/auth.py with UserCreate (email EmailStr, name, password with validators), UserLogin (email, password), UserResponse (id, email, name, created_at), TokenResponse (access_token, refresh_token, token_type, expires_in)
- [X] T016 [P] Create backend Pydantic task schemas in backend/src/schemas/task.py with TaskCreate (title max 200 validated, description max 2000), TaskUpdate (title optional, description optional), TaskResponse (id, title, description, completed, created_at, updated_at)
- [X] T017 Create backend auth service in backend/src/services/auth_service.py with functions: hash_password(password) using bcrypt 12 rounds, verify_password(password, hashed), create_access_token(user_id) 15-min expiry, create_refresh_token(user_id) 7-day expiry, verify_token(token) using pyjwt
- [X] T018 Create backend dependency injection module in backend/src/api/deps.py with get_db_session() dependency (yields SQLModel Session), get_current_user(token: HTTPBearer) dependency (verifies JWT, queries User by user_id from token payload, raises 401 if invalid)
- [X] T019 [P] Create frontend API client utility in frontend/src/lib/api.ts with fetch wrapper functions (get, post, put, delete, patch) that automatically add Authorization Bearer token header from cookies/storage, handle JSON serialization, throw errors on non-2xx responses
- [X] T020 [P] Create frontend TypeScript types in frontend/src/types/auth.ts for User, LoginRequest, SignupRequest, TokenResponse matching backend schemas
- [X] T021 [P] Create frontend TypeScript types in frontend/src/types/task.ts for Task, TaskCreate, TaskUpdate matching backend schemas
- [X] T022 [P] Create frontend root layout in frontend/src/app/layout.tsx with metadata, fonts, Tailwind CSS imports, RootProvider wrapper for Better Auth context
- [X] T023 [P] Create frontend middleware in frontend/src/middleware.ts to protect /dashboard routes by checking for JWT access_token cookie, redirect to /login if missing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in with JWT authentication, and log out, with secure password hashing and session management

**Independent Test**: Create account via signup form with valid credentials (email, name, password meeting requirements), verify redirect to login, log in with credentials, verify JWT token issued and dashboard accessible, log out and verify token invalidated

### Tests for User Story 1 (Backend pytest) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T024 [P] [US1] Create pytest fixtures in backend/tests/conftest.py: test_db_session (in-memory SQLite for testing), test_client (FastAPI TestClient), auth_headers (helper to generate valid JWT for authenticated requests)
- [X] T025 [P] [US1] Unit test for User model validation in backend/tests/unit/test_models.py: test_user_email_uniqueness, test_user_password_hash_required, test_user_created_at_auto_generated
- [X] T026 [P] [US1] Unit test for auth service in backend/tests/unit/test_services.py: test_hash_password_bcrypt, test_verify_password_success, test_verify_password_failure, test_create_access_token_15min_expiry, test_create_refresh_token_7day_expiry, test_verify_token_valid, test_verify_token_expired, test_verify_token_invalid
- [X] T027 [US1] Integration test for signup endpoint in backend/tests/integration/test_auth_api.py: test_signup_success_201, test_signup_duplicate_email_400, test_signup_weak_password_400 (missing uppercase/lowercase/number), test_signup_invalid_email_400

### Implementation for User Story 1

- [X] T028 [US1] Implement auth service signup function in backend/src/services/auth_service.py: signup_user(session, email, name, password) that validates password requirements (min 8 chars, 1 uppercase, 1 lowercase, 1 number), hashes password with bcrypt, creates User record, returns UserResponse
- [X] T029 [US1] Implement auth service login function in backend/src/services/auth_service.py: login_user(session, email, password) that queries User by email, verifies password with bcrypt, creates access_token and refresh_token, returns TokenResponse with tokens and expiry
- [X] T030 [US1] Create auth API router in backend/src/api/auth.py with APIRouter prefix="/api/auth", implement POST /signup endpoint (accepts UserCreate schema, calls auth_service.signup_user, returns 201 with UserResponse)
- [X] T031 [US1] Implement POST /login endpoint in backend/src/api/auth.py (accepts UserLogin schema, calls auth_service.login_user, returns 200 with TokenResponse including access_token and refresh_token, handles 401 for invalid credentials)
- [X] T032 [US1] Implement POST /logout endpoint in backend/src/api/auth.py (requires JWT authentication via Depends(get_current_user), invalidates refresh token if using token blacklist or simply returns 200 success for stateless JWT)
- [X] T033 [US1] Implement GET /me endpoint in backend/src/api/auth.py (requires Depends(get_current_user), returns current UserResponse from JWT payload)
- [X] T034 [US1] Register auth APIRouter in backend/src/main.py app.include_router(auth_router)
- [X] T035 [P] [US1] Create frontend login page in frontend/src/app/login/page.tsx as Client Component with LoginForm, redirect to /dashboard on success, link to /signup
- [X] T036 [P] [US1] Create frontend signup page in frontend/src/app/signup/page.tsx as Client Component with SignupForm, redirect to /login on success, link to /login
- [X] T037 [US1] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx with shadcn/ui Input and Button, handle form submission calling POST /api/auth/login via api.ts, store access_token in httpOnly cookie or secure storage, display error messages for 401, redirect to /dashboard on 200
- [X] T038 [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx with shadcn/ui Input and Button, client-side password validation (min 8 chars, 1 uppercase, 1 lowercase, 1 number) with real-time feedback, handle form submission calling POST /api/auth/signup, display success message and redirect to /login, display error messages for 400 (duplicate email, weak password)
- [X] T039 [US1] Create Header component in frontend/src/components/shared/Header.tsx with app title, user name display (from GET /api/auth/me), Logout button that calls POST /api/auth/logout, clears tokens, redirects to /login
- [X] T040 [US1] Add Header component to protected dashboard layout in frontend/src/app/dashboard/layout.tsx
- [X] T041 [US1] Create landing page in frontend/src/app/page.tsx that redirects authenticated users to /dashboard, unauthenticated users to /login (check for JWT token)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - users can sign up, log in, access protected dashboard, log out

---

## Phase 4: User Story 2 - Task Management with Persistence (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create, view, update, delete, and toggle tasks via web UI with PostgreSQL persistence and user isolation

**Independent Test**: Log in, create multiple tasks via web form, verify tasks appear in list sorted (incomplete first, newest within groups), edit task title/description, toggle task completion with checkbox, delete task with modal confirmation, log out and log back in to verify tasks persist, verify user isolation (different users cannot see each other's tasks)

### Tests for User Story 2 (Backend pytest) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T042 [P] [US2] Unit test for Task model validation in backend/tests/unit/test_models.py: test_task_title_max_200, test_task_description_max_2000, test_task_user_id_required, test_task_completed_default_false
- [X] T043 [P] [US2] Unit test for task service in backend/tests/unit/test_services.py: test_create_task_with_user_id, test_get_user_tasks_filtered_by_user_id, test_get_user_tasks_sorted_incomplete_first_newest_first, test_update_task_with_authorization_check, test_delete_task_with_authorization_check, test_toggle_task_completion
- [X] T044 [US2] Integration test for task CRUD endpoints in backend/tests/integration/test_tasks_api.py: test_create_task_201_authenticated, test_create_task_401_unauthenticated, test_get_tasks_200_user_isolated (create tasks for 2 users, verify each sees only their own), test_get_tasks_sorted_incomplete_first, test_update_task_200_authorized, test_update_task_404_unauthorized (try to update another user's task), test_delete_task_200_authorized, test_delete_task_404_unauthorized, test_toggle_task_200

### Implementation for User Story 2

- [X] T045 [P] [US2] Create task service in backend/src/services/task_service.py with create_task(session, user_id, title, description) that validates title non-empty max 200, description max 2000, creates Task with user_id, returns TaskResponse
- [X] T046 [P] [US2] Implement get_user_tasks(session, user_id) in backend/src/services/task_service.py that queries Task filtered by user_id, ordered by completed ASC then created_at DESC per FR-009, returns list of TaskResponse
- [X] T047 [US2] Implement update_task(session, task_id, user_id, title, description) in backend/src/services/task_service.py that queries Task by id AND user_id (authorization check), raises 404 if not found, updates fields if provided, updates updated_at timestamp, returns TaskResponse
- [X] T048 [US2] Implement delete_task(session, task_id, user_id) in backend/src/services/task_service.py that queries Task by id AND user_id, raises 404 if not found, deletes task, returns success
- [X] T049 [US2] Implement toggle_task_completion(session, task_id, user_id) in backend/src/services/task_service.py that queries Task by id AND user_id, raises 404 if not found, toggles completed boolean, updates updated_at, returns TaskResponse
- [X] T050 [US2] Create tasks API router in backend/src/api/tasks.py with APIRouter prefix="/api/tasks", all endpoints require Depends(get_current_user) for JWT authentication
- [X] T051 [US2] Implement GET /api/tasks endpoint in backend/src/api/tasks.py (calls task_service.get_user_tasks with current_user.id, returns 200 with list of TaskResponse)
- [X] T052 [US2] Implement POST /api/tasks endpoint in backend/src/api/tasks.py (accepts TaskCreate schema, calls task_service.create_task with current_user.id, returns 201 with TaskResponse)
- [X] T053 [US2] Implement PUT /api/tasks/{id} endpoint in backend/src/api/tasks.py (accepts TaskUpdate schema, calls task_service.update_task with task_id and current_user.id, returns 200 with TaskResponse, handles 404 for unauthorized access)
- [X] T054 [US2] Implement DELETE /api/tasks/{id} endpoint in backend/src/api/tasks.py (calls task_service.delete_task with task_id and current_user.id, returns 200 success, handles 404 for unauthorized access per FR-025)
- [X] T055 [US2] Implement PATCH /api/tasks/{id}/toggle endpoint in backend/src/api/tasks.py (calls task_service.toggle_task_completion with task_id and current_user.id, returns 200 with TaskResponse)
- [X] T056 [US2] Register tasks APIRouter in backend/src/main.py app.include_router(tasks_router)
- [X] T057 [P] [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx as Server Component that fetches initial tasks from GET /api/tasks server-side (with auth headers from cookies), passes to TaskList Client Component, displays empty state "No tasks yet. Create your first task!" if no tasks
- [X] T058 [US2] Create TaskList Client Component in frontend/src/components/tasks/TaskList.tsx with useState for tasks array, map tasks to TaskItem components, handle create/update/delete/toggle events with API calls, update local state optimistically
- [X] T059 [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx as shadcn/ui Card with task title, description, checkbox for completion toggle (calls PATCH /api/tasks/{id}/toggle), Edit button (opens TaskForm in edit mode), Delete button (opens DeleteConfirmModal), apply strikethrough or visual indicator for completed tasks
- [X] T060 [US2] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx as shadcn/ui Dialog with Input fields for title (max 200 chars with counter), description (max 2000 chars with counter), client-side validation (title required), submit calls POST /api/tasks (create mode) or PUT /api/tasks/{id} (edit mode), handle 400/401 errors, close dialog on success
- [X] T061 [US2] Create DeleteConfirmModal component in frontend/src/components/tasks/DeleteConfirmModal.tsx as shadcn/ui AlertDialog with title "Delete Task", description "Are you sure? This action cannot be undone.", Cancel button (secondary), Delete button (danger red bg-destructive), on confirm calls DELETE /api/tasks/{id}, closes modal on success
- [X] T062 [US2] Add "Add Task" button to dashboard page in frontend/src/app/dashboard/page.tsx that opens TaskForm in create mode

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can manage tasks with full CRUD operations, data persists across sessions, user isolation is enforced

---

## Phase 5: User Story 3 - Responsive Web Interface with Modern UX (Priority: P2)

**Goal**: Polished, responsive UI that works on desktop, tablet, and mobile with shadcn/ui components, keyboard navigation, loading states, and accessibility

**Independent Test**: Access application on desktop (1920px), tablet (768px), and mobile (375px) viewports, verify responsive layouts (stacked on mobile, grid on desktop), test keyboard navigation (Tab, Enter, Escape) for all interactive elements, verify loading states during API calls (spinners, disabled buttons), test with screen reader for ARIA labels

### Implementation for User Story 3

- [X] T063 [P] [US3] Make TaskList responsive in frontend/src/components/tasks/TaskList.tsx: use Tailwind grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 for task cards, stack vertically on mobile
- [X] T064 [P] [US3] Make TaskItem responsive in frontend/src/components/tasks/TaskItem.tsx: ensure buttons have min-h-[44px] min-w-[44px] for touch targets on mobile, add hover states for desktop (hover:bg-accent)
- [X] T065 [P] [US3] Make Header responsive in frontend/src/components/shared/Header.tsx: stack elements vertically on mobile (flex flex-col sm:flex-row), hide user name on mobile if needed, ensure Logout button is touch-friendly
- [X] T066 [US3] Add keyboard navigation to TaskForm in frontend/src/components/tasks/TaskForm.tsx: Escape key closes dialog, Enter key submits form (when in input fields), focus trap within dialog, auto-focus title input on open
- [X] T067 [US3] Add keyboard navigation to DeleteConfirmModal in frontend/src/components/tasks/DeleteConfirmModal.tsx: Escape key closes modal, Enter key confirms delete, Tab cycles between Cancel and Delete buttons
- [X] T068 [US3] Create LoadingSpinner component in frontend/src/components/shared/LoadingSpinner.tsx using lucide-react Loader2 icon with animate-spin, use for loading states
- [X] T069 [US3] Add loading states to TaskList in frontend/src/components/tasks/TaskList.tsx: show LoadingSpinner during initial fetch, disable buttons during API operations, show skeleton loaders for pending tasks
- [X] T070 [US3] Add loading states to TaskForm in frontend/src/components/tasks/TaskForm.tsx: disable submit button during API call, show loading spinner on button, prevent double submission
- [X] T071 [US3] Add real-time validation feedback to SignupForm in frontend/src/components/auth/SignupForm.tsx: show password requirements checklist (8 chars, uppercase, lowercase, number) with green checkmarks as user types, highlight invalid fields with red border
- [X] T072 [US3] Add ARIA labels and semantic HTML to all components: label inputs with <Label> from shadcn/ui, add aria-label to icon buttons, use semantic <button> elements, ensure heading hierarchy (h1, h2, h3)

**Checkpoint**: All user stories should now have polished, responsive UI that works across devices with keyboard navigation and accessibility support

---

## Phase 6: User Story 4 - Error Handling and User Feedback (Priority: P2)

**Goal**: Clear, user-friendly error messages and success feedback for all operations, graceful handling of network errors, session expiration, and validation errors

**Independent Test**: Simulate error conditions - submit empty task title (see client-side validation error), let JWT expire (see session expired message and redirect to login), try to access another user's task by guessing ID (see 404 not found), disconnect network (see connection error message), complete successful operations (see success toast notifications)

### Implementation for User Story 4

- [X] T073 [P] [US4] Create toast notification system in frontend/src/app/layout.tsx: add shadcn/ui Toaster component to root layout, configure toast position (bottom-right)
- [X] T074 [P] [US4] Create error handling utility in frontend/src/lib/utils.ts: handleApiError(error) function that extracts error message from API response (400/401/404/500), formats user-friendly messages, returns toast-ready message
- [X] T075 [US4] Add client-side validation to TaskForm in frontend/src/components/tasks/TaskForm.tsx: validate title non-empty before API call, show error message "Title is required" below input field, prevent submission if invalid
- [X] T076 [US4] Add JWT expiration handling to API client in frontend/src/lib/api.ts: catch 401 responses, check if error is "token expired", clear stored tokens, show toast "Session expired, please log in again", redirect to /login
- [X] T077 [US4] Add network error handling to API client in frontend/src/lib/api.ts: wrap fetch in try-catch, catch network errors (fetch failure), show toast "Unable to connect to server. Please try again later."
- [X] T078 [US4] Add success notifications to TaskList in frontend/src/components/tasks/TaskList.tsx: show toast "Task created successfully" after POST, "Task updated successfully" after PUT, "Task deleted successfully" after DELETE, "Task marked as complete" after PATCH toggle
- [X] T079 [US4] Add error notifications to TaskList in frontend/src/components/tasks/TaskList.tsx: show toast with error message from handleApiError() if any CRUD operation fails (400/404/500)
- [X] T080 [US4] Add error notifications to LoginForm in frontend/src/components/auth/LoginForm.tsx: show toast "Invalid credentials" for 401, show generic error for 500, show network error for fetch failure
- [X] T081 [US4] Add error notifications to SignupForm in frontend/src/components/auth/SignupForm.tsx: show toast "Email already registered" for 400 with duplicate email error, show password validation errors inline, show generic error for 500
- [X] T082 [US4] Update backend error responses to be user-friendly: in backend/src/api/auth.py and backend/src/api/tasks.py, ensure HTTPException detail messages are clear (e.g., "Invalid credentials" not "Authentication failed", "Task not found" not "404")
- [X] T083 [US4] Add empty state message to dashboard in frontend/src/app/dashboard/page.tsx: when tasks array is empty, show Card with message "No tasks yet. Create your first task!" with prominent "Add Task" button

**Checkpoint**: All error paths should now display clear, actionable messages to users, and all successful operations should provide visual feedback

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories, documentation, and deployment readiness

- [X] T084 [P] Create backend README.md in backend/README.md with setup instructions (venv, requirements.txt, .env configuration, database initialization, uvicorn start command), reference quickstart.md
- [X] T085 [P] Create frontend README.md in frontend/README.md with setup instructions (npm install, .env.local configuration, npm run dev), reference quickstart.md
- [X] T086 [P] Add comprehensive inline code comments to backend services: backend/src/services/auth_service.py and backend/src/services/task_service.py with docstrings for all functions, parameter descriptions, return types
- [X] T087 [P] Add TypeScript JSDoc comments to frontend components: document props interfaces, complex functions, usage examples in comments
- [X] T088 Create backend API documentation endpoint in backend/src/main.py: configure FastAPI to expose OpenAPI docs at /docs (Swagger UI) and /openapi.json, add metadata (title, description, version)
- [X] T089 [P] Add logging to backend operations in backend/src/services/task_service.py and backend/src/services/auth_service.py: log user signup, login, task CRUD operations with user_id for audit trail, use Python logging module
- [X] T090 [P] Add security headers to backend in backend/src/main.py: add middleware for X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection: 1; mode=block
- [X] T091 Validate quickstart.md by following setup instructions end-to-end: provision Neon database, create .env files, run backend (verify health check), run frontend (verify login/signup/dashboard), document any missing steps
- [X] T092 Create deployment checklist in specs/002-fullstack-web-auth/deployment.md: environment variables required, database migration steps, production .env examples, CORS configuration for production origin, SSL/HTTPS requirements
- [X] T093 Run backend pytest suite: pytest backend/tests/ -v, verify all unit and integration tests pass (auth, tasks, models, services), fix any failing tests, aim for >80% code coverage
- [X] T094 Manual frontend testing checklist: test signup with invalid passwords, test login with incorrect credentials, test task CRUD on mobile viewport (375px), test keyboard navigation, test session expiration (wait 15+ minutes), verify no console errors, verify responsive breakpoints (mobile 375px, tablet 768px, desktop 1920px)
- [X] T095 Update root README.md with Phase II completion status: add "Phase II: ✅ Complete" badge, link to quickstart.md, add screenshots of login/dashboard, document Phase III roadmap

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T009) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T010-T023) - Authentication foundation
- **User Story 2 (Phase 4)**: Depends on Foundational (T010-T023) AND User Story 1 (T024-T041 for authentication) - Task management requires authenticated users
- **User Story 3 (Phase 5)**: Depends on User Story 2 (T042-T062) - UI polish requires functional task management
- **User Story 4 (Phase 6)**: Depends on User Story 1 and 2 (T024-T062) - Error handling enhances existing flows
- **Polish (Phase 7)**: Depends on all user stories being complete (T024-T083)

### User Story Dependencies

- **User Story 1 (P1 MVP)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 MVP)**: Depends on Foundational (Phase 2) AND User Story 1 (for authentication) - Tasks require authenticated users
- **User Story 3 (P2)**: Depends on User Story 2 - Responsive UI enhances task management
- **User Story 4 (P2)**: Depends on User Story 1 and 2 - Error handling enhances auth and task flows

### Within Each User Story

- **User Story 1**: Tests (T024-T027) → Auth service (T028-T029) → Auth API (T030-T034) → Frontend pages/components (T035-T041)
- **User Story 2**: Tests (T042-T044) → Task service (T045-T049) → Task API (T050-T056) → Frontend dashboard/components (T057-T062)
- **User Story 3**: Frontend responsive updates (T063-T072) can run in parallel
- **User Story 4**: Frontend error handling (T073-T083) can run in parallel after utility setup (T073-T074)

### Parallel Opportunities

- **Setup (Phase 1)**: T003-T004 (frontend init), T005-T006 (env templates), T007-T008 (Tailwind/shadcn) can run in parallel
- **Foundational (Phase 2)**: T013-T014 (models), T015-T016 (schemas), T019-T023 (frontend setup) can run in parallel after database setup (T010-T012)
- **User Story 1 Tests**: T024-T027 can all run in parallel
- **User Story 1 Frontend**: T035-T036 (pages), T037-T038 (forms) can run in parallel
- **User Story 2 Tests**: T042-T043 can run in parallel
- **User Story 2 Service**: T045-T046 can run in parallel
- **User Story 3**: T063-T065 (responsive layouts), T066-T067 (keyboard nav), T068-T072 (loading/accessibility) can run in parallel
- **User Story 4**: T073-T074 (utilities), T075-T083 (error handling per component) can run in parallel
- **Polish**: T084-T087 (docs/comments), T089-T090 (logging/security) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# After T010-T012 (database setup) complete, launch in parallel:
Task: "Create backend User SQLModel in backend/src/models/user.py"
Task: "Create backend Task SQLModel in backend/src/models/task.py"
Task: "Create backend Pydantic auth schemas in backend/src/schemas/auth.py"
Task: "Create backend Pydantic task schemas in backend/src/schemas/task.py"
Task: "Create frontend API client utility in frontend/src/lib/api.ts"
Task: "Create frontend TypeScript types in frontend/src/types/auth.ts"
Task: "Create frontend TypeScript types in frontend/src/types/task.ts"
Task: "Create frontend root layout in frontend/src/app/layout.tsx"
Task: "Create frontend middleware in frontend/src/middleware.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T023) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T024-T041) - Authentication
4. Complete Phase 4: User Story 2 (T042-T062) - Task management
5. **STOP and VALIDATE**: Test both stories independently (signup → login → create tasks → logout → login → verify persistence)
6. MVP ready - can deploy/demo with core functionality

### Incremental Delivery

1. Complete Setup + Foundational (T001-T023) → Foundation ready
2. Add User Story 1 (T024-T041) → Test independently → MVP Auth ready
3. Add User Story 2 (T042-T062) → Test independently → MVP Complete (can deploy/demo)
4. Add User Story 3 (T063-T072) → Test independently → UI polish complete
5. Add User Story 4 (T073-T083) → Test independently → Production-ready UX
6. Add Polish (T084-T095) → Documentation and deployment ready
7. Each phase adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T023)
2. Once Foundational is done (T023 complete):
   - Developer A: User Story 1 Backend (T024-T034)
   - Developer B: User Story 1 Frontend (T035-T041)
   - Integration point: Auth API complete
3. User Story 1 complete, then:
   - Developer A: User Story 2 Backend (T042-T056)
   - Developer B: User Story 2 Frontend (T057-T062)
   - Integration point: Task API complete
4. User Story 2 complete, then:
   - Developer A: User Story 3 (T063-T072)
   - Developer B: User Story 4 (T073-T083)
   - Parallel execution: No dependencies between US3 and US4
5. Both complete, then:
   - Developer A: Polish backend (T086, T089-T090, T093)
   - Developer B: Polish frontend (T087, T094-T095)
   - Shared: Documentation (T084-T085, T091-T092)

---

## Notes

- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability (US1=User Story 1, US2=User Story 2, US3=User Story 3, US4=User Story 4)
- **Each user story**: Independently completable and testable
- **Backend tests**: Write tests FIRST (TDD), ensure they FAIL before implementation, pytest for unit/integration tests
- **Frontend testing**: Manual testing acceptable per user requirements, focus on user flows and responsive design
- **User isolation**: ALL backend queries MUST filter by user_id from JWT token (enforced in task service layer)
- **Quality gates**: Phase II FAILS if any button is non-functional, UI looks unfinished, auth is bypassable, tasks leak across users, or specs are ignored
- **Commit strategy**: Commit after each task or logical group (e.g., T010-T012 database setup, T030-T034 auth API, T050-T056 task API)
- **Stop at checkpoints**: Validate each user story independently before proceeding to next priority
- **Avoid**: Vague tasks, same-file conflicts, cross-story dependencies that break independence, hardcoded secrets, raw SQL queries
