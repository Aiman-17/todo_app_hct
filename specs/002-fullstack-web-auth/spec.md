# Feature Specification: Phase II - Full-Stack Web Application with Authentication

**Feature Branch**: `002-fullstack-web-auth`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Phase II: Full-stack web application with Next.js 16+ frontend, FastAPI backend, Neon PostgreSQL persistence, and JWT authentication using Better Auth"

## Clarifications

### Session 2025-12-30

- Q: What password validation rules should be enforced during user registration? → A: Minimum 8 characters, must include uppercase, lowercase, and number (balanced security)
- Q: What should be the JWT access token expiration time and refresh token strategy? → A: Access token: 15 minutes, Refresh token: 7 days (balanced approach, industry standard)
- Q: What are the maximum character length limits for task title and description fields? → A: Title: 200 characters max, Description: 2000 characters max (balanced, prevents abuse while allowing detail)
- Q: What UX pattern should be used for the task delete confirmation to prevent accidental data loss? → A: Modal dialog with Delete (danger) and Cancel buttons, using modern UI components (shadcn/ui)
- Q: What should be the default sort order for tasks on the dashboard? → A: Incomplete tasks first, then newest first within each group (descending by creation date) - prioritizes active tasks while keeping recent items visible

## Technology Stack (Authoritative)

**This section is MANDATORY and NON-NEGOTIABLE. All implementation must strictly follow these specifications.**

### Frontend Stack

- **Framework**: Next.js 16+ (App Router mandatory)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + lucide-react
- **Authentication**: Better Auth (client-side)
- **Communication**: HTTP REST calls to backend `/api/*` endpoints
- **Token Management**: JWT access token (15 min expiration) and refresh token (7 day expiration) stored in httpOnly cookies or secure storage
- **Environment**: BETTER_AUTH_SECRET (shared with backend)

**Critical Frontend Rules**:
- NO direct database access
- ALL data operations go through backend API
- JWT token required on every backend request
- App Router structure: `/app/*` directories
- Server Components where possible, Client Components only when needed

### Backend Stack

- **Framework**: FastAPI
- **Language**: Python 3.13+
- **Server**: Uvicorn
- **ORM**: SQLModel (MANDATORY - do not use SQLAlchemy Core or raw SQL)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (server-side validation)
- **Token**: JWT access token (15 min expiration) verified on every request; refresh token (7 day expiration) for renewing access tokens
- **API Pattern**: APIRouter for domain grouping
- **Environment**: BETTER_AUTH_SECRET (shared with frontend)

**Critical Backend Rules**:
- MUST use SQLModel for all database operations
- NO raw SQL queries
- JWT validation middleware on all protected routes
- RESTful API design under `/api/*`
- Domain-grouped routes (e.g., `/api/tasks/*`, `/api/auth/*`, `/api/health`)
- Proper error handling with HTTP status codes
- CORS configured for frontend origin

### Database Schema

**Users Table** (managed by Better Auth):
- `id` (UUID primary key)
- `email` (unique, indexed)
- `name` (string)
- `password_hash` (bcrypt)
- `created_at` (timestamp)
- `updated_at` (timestamp)

**Tasks Table** (extends Phase I model):
- `id` (integer primary key, auto-increment)
- `user_id` (UUID foreign key to users.id) ← **NEW: user isolation**
- `title` (string, required, max 200 characters)
- `description` (text, optional, max 2000 characters)
- `completed` (boolean, default false)
- `created_at` (timestamp)
- `updated_at` (timestamp)

**Critical Database Rules**:
- ALL task queries MUST filter by `user_id` from JWT token
- NO cross-user data access
- Indexes on `user_id` and `completed` columns
- Use Neon connection pooling

### Communication Protocol

- **Transport**: HTTP REST
- **Data Format**: JSON
- **Authentication**: JWT in Authorization header (`Bearer <token>`)
- **Base URL**: Backend at `/api/`, frontend at root `/`
- **CORS**: Configured to allow frontend origin

**API Conventions**:
- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login (returns access + refresh tokens)
- `POST /api/auth/refresh` - Refresh access token using refresh token
- `POST /api/auth/logout` - User logout (invalidates refresh token)
- `GET /api/auth/me` - Get current user

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - User Registration and Authentication (Priority: P1)

As a new user, I want to create an account and log in so that I can manage my personal todo tasks securely.

**Why this priority**: Authentication is the foundation of Phase II. Without user accounts, we cannot provide data isolation or persistence. This is the minimal viable feature that differentiates Phase II from Phase I.

**Independent Test**: Can be fully tested by creating a new account via signup form, logging in with credentials, and verifying JWT token is issued. User should see a protected dashboard after login.

**Acceptance Scenarios**:

1. **Given** I am on the signup page, **When** I enter valid email, name, and password, **Then** my account is created and I am redirected to the login page
2. **Given** I have an account, **When** I enter correct email and password on login page, **Then** I receive a JWT token and am redirected to the tasks dashboard
3. **Given** I am logged in, **When** I click logout, **Then** my JWT token is invalidated and I am redirected to the login page
4. **Given** I enter an email that already exists during signup, **When** I submit the form, **Then** I see error message "Email already registered"
5. **Given** I enter incorrect password during login, **When** I submit the form, **Then** I see error message "Invalid credentials"

---

### User Story 2 - Task Management with Persistence (Priority: P1)

As an authenticated user, I want to create, view, update, and delete my todo tasks in a web interface, with all changes saved to the database so that my tasks persist across sessions.

**Why this priority**: This is the core functionality that combines Phase I CRUD operations with web UI and database persistence. It delivers immediate user value and represents the minimum viable product for Phase II.

**Independent Test**: Can be fully tested by logging in, creating multiple tasks via web form, logging out, logging back in, and verifying tasks are still present. All CRUD operations (create, read, update, delete, toggle) should work through the web UI.

**Acceptance Scenarios**:

1. **Given** I am logged in to the dashboard, **When** I click "Add Task" and enter title and description, **Then** the task appears in my task list immediately and is saved to database
2. **Given** I have existing tasks, **When** I view my dashboard, **Then** I see only my tasks (filtered by user_id), with incomplete tasks first, then completed tasks, each group sorted newest first (descending by creation date)
3. **Given** I have a task, **When** I click "Edit" and update the title or description, **Then** the changes are saved and reflected immediately
4. **Given** I have a task, **When** I click the checkbox to toggle completion, **Then** the task status updates and the UI reflects the change (strikethrough or visual indicator)
5. **Given** I have a task, **When** I click "Delete", a modal dialog appears with "Delete" (danger) and "Cancel" buttons, and I click "Delete", **Then** the task is removed from both UI and database
6. **Given** I log out and log back in, **When** I view my dashboard, **Then** all my previously created tasks are still present

---

### User Story 3 - Responsive Web Interface with Modern UX (Priority: P2)

As a user, I want a clean, responsive web interface built with modern UI components so that I can manage tasks efficiently on any device (desktop, tablet, mobile).

**Why this priority**: While core functionality is P1, good UX significantly improves adoption and usability. This story focuses on the visual polish and responsive design using shadcn/ui components.

**Independent Test**: Can be fully tested by accessing the application on different screen sizes (desktop, tablet, mobile) and verifying all components render correctly and are accessible via keyboard and screen readers.

**Acceptance Scenarios**:

1. **Given** I am on the task dashboard, **When** I view it on mobile (< 768px), **Then** the layout stacks vertically and all buttons are touch-friendly (min 44px tap targets)
2. **Given** I am on the task dashboard, **When** I view it on desktop, **Then** tasks are displayed in a responsive grid or list with hover states
3. **Given** I am creating/editing a task, **When** I interact with the form, **Then** I see real-time validation feedback and clear error messages
4. **Given** I am using the application, **When** I navigate via keyboard only (Tab, Enter, Escape), **Then** all interactive elements are accessible and focus indicators are visible
5. **Given** a task operation is in progress, **When** the backend request is pending, **Then** I see a loading state (spinner or skeleton) and cannot double-submit

---

### User Story 4 - Error Handling and User Feedback (Priority: P2)

As a user, I want clear error messages and feedback when something goes wrong so that I understand what happened and how to fix it.

**Why this priority**: Good error handling is critical for production readiness but not essential for MVP. This ensures users aren't confused by technical errors.

**Independent Test**: Can be tested by simulating error conditions (network failure, invalid input, unauthorized access) and verifying user-friendly error messages are displayed.

**Acceptance Scenarios**:

1. **Given** I submit a task with empty title, **When** the form validates, **Then** I see error message "Title is required" without backend call
2. **Given** I am logged in and my JWT expires, **When** I make any API request, **Then** I am redirected to login page with message "Session expired, please log in again"
3. **Given** I try to access another user's task by guessing the ID, **When** the backend validates the request, **Then** I receive 404 Not Found (to prevent information leakage)
4. **Given** the backend is unreachable, **When** I try any operation, **Then** I see error message "Unable to connect to server. Please try again later."
5. **Given** I successfully complete an operation, **When** the request completes, **Then** I see a success toast/notification (e.g., "Task created successfully")

---

### Edge Cases

- **What happens when a user tries to register with a weak password?** Frontend validates password requirements (min 8 chars, uppercase, lowercase, number) before submission, backend rejects with 400 Bad Request and specific error message
- **What happens when a user tries to register with an invalid email format?** Frontend validates email format before submission, backend rejects with 400 Bad Request
- **What happens when JWT token is tampered with?** Backend JWT verification fails, returns 401 Unauthorized, frontend redirects to login
- **What happens when two users have tasks with the same ID?** IDs are globally unique (auto-increment), but all queries filter by `user_id` to ensure isolation
- **What happens when database connection fails?** Backend returns 503 Service Unavailable, frontend shows retry option
- **What happens when user deletes all tasks?** Dashboard shows empty state with "No tasks yet. Create your first task!" message
- **What happens when user enters title exceeding 200 characters or description exceeding 2000 characters?** Frontend enforces max length, backend validates and returns 400 Bad Request with specific field error
- **What happens during concurrent task updates?** Last write wins (optimistic concurrency), future enhancement could add version/timestamp checks

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create accounts with email, name, and password
- **FR-002**: System MUST validate email format and enforce unique email constraint
- **FR-003**: System MUST enforce password validation: minimum 8 characters with at least one uppercase letter, one lowercase letter, and one number
- **FR-004**: System MUST hash passwords using bcrypt before storing in database
- **FR-005**: System MUST authenticate users via email/password and issue JWT tokens (access token: 15 min expiration, refresh token: 7 day expiration)
- **FR-006**: System MUST provide token refresh endpoint to renew access tokens using valid refresh tokens
- **FR-007**: System MUST verify JWT token on every protected API request
- **FR-008**: System MUST filter all task queries by authenticated user's `user_id`
- **FR-009**: System MUST return tasks sorted with incomplete tasks first, then completed tasks, each group ordered newest first (descending by created_at)
- **FR-010**: System MUST provide CRUD operations for tasks via RESTful API endpoints
- **FR-011**: System MUST validate task fields: title (required, max 200 chars), description (optional, max 2000 chars)
- **FR-012**: Frontend MUST display modal confirmation dialog (using shadcn/ui) with "Delete" (danger) and "Cancel" buttons before deleting tasks
- **FR-013**: System MUST persist all task data to Neon PostgreSQL database using SQLModel
- **FR-014**: Frontend MUST communicate with backend exclusively via `/api/*` HTTP endpoints
- **FR-015**: System MUST use Better Auth with shared `BETTER_AUTH_SECRET` for both frontend and backend
- **FR-016**: System MUST implement proper CORS configuration to allow frontend origin
- **FR-017**: System MUST return appropriate HTTP status codes (200, 201, 400, 401, 404, 500)
- **FR-018**: Frontend MUST use Next.js App Router with TypeScript and Tailwind CSS
- **FR-019**: Frontend MUST use shadcn/ui components for all UI elements
- **FR-020**: Backend MUST use FastAPI with APIRouter pattern for domain-grouped routes
- **FR-021**: System MUST handle logout by invalidating JWT refresh token
- **FR-022**: System MUST provide user profile endpoint (`/api/auth/me`) to get current user info
- **FR-023**: Tasks table MUST include `user_id` foreign key to enforce user isolation
- **FR-024**: System MUST auto-populate `created_at` and `updated_at` timestamps
- **FR-025**: System MUST prevent cross-user data access through authorization checks

### Key Entities

- **User**: Represents an authenticated user account with email, name, password hash, and timestamps. Managed by Better Auth.
- **Task**: Represents a todo item owned by a specific user, with title, description, completion status, and timestamps. Extends Phase I model with `user_id` foreign key.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 1 minute
- **SC-002**: Users can log in and see their task dashboard in under 5 seconds
- **SC-003**: All CRUD operations (create, read, update, delete, toggle) complete in under 2 seconds
- **SC-004**: Application is responsive and usable on screen sizes from 320px to 1920px width
- **SC-005**: No cross-user data leakage - users can only access their own tasks
- **SC-006**: 100% of API endpoints protected by JWT authentication
- **SC-007**: All forms provide real-time validation feedback
- **SC-008**: Application works correctly with JavaScript-enabled browsers (Chrome, Firefox, Safari, Edge latest versions)
- **SC-009**: Database schema includes proper indexes for query performance (user_id, completed)
- **SC-010**: All user actions provide visual feedback (loading states, success/error messages)

## Constraints

- Frontend MUST NOT access database directly
- Backend MUST use SQLModel, NO raw SQL
- Authentication MUST use Better Auth with JWT
- Database MUST be Neon Serverless PostgreSQL
- Frontend MUST use Next.js 16+ App Router
- All protected routes MUST verify JWT token
- Tasks MUST be isolated by user_id
- No broken links and warnings 
 