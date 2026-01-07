# ADR-0003: Authentication Architecture - JWT-Based Auth with Better Auth and bcrypt

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Authentication Architecture" not separate ADRs for JWT, password hashing, token storage).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 002-fullstack-web-auth
- **Context:** Phase II requires secure user authentication with multi-device support (web, future mobile), password-based signup/login, and stateless API design. Authentication must protect all task operations and enforce user data isolation.

## Decision

**Adopt JWT-based authentication with Better Auth SDK (Python + TypeScript), bcrypt password hashing (12 salt rounds), httpOnly cookies for token storage, and dual-token strategy (15-minute access tokens, 7-day refresh tokens).**

Architecture Components:
- **Authentication Library:** Better Auth SDK (framework-agnostic, supports Python backend + React frontend)
- **Token Type:** JWT (JSON Web Tokens) with HS256 algorithm (HMAC with SHA-256)
- **Password Hashing:** bcrypt with 12 salt rounds (industry-standard one-way hashing)
- **Token Storage:** httpOnly cookies (prevents XSS token theft, auto-sent with requests)
- **Token Lifetimes:** Access token: 15 minutes (short-lived), Refresh token: 7 days (long-lived)
- **Shared Secret:** BETTER_AUTH_SECRET environment variable (min 32 characters, same in backend + frontend)
- **Token Refresh Flow:** Automatic client-side refresh when access token expires (Better Auth SDK handles this)
- **User Isolation:** All database queries filter by `user_id` extracted from JWT payload
- **Logout:** Invalidate refresh token server-side, access token expires naturally (15 min)

## Consequences

### Positive

- **Stateless API:** JWT tokens contain user_id claim, eliminating need for server-side session storage (scales horizontally without sticky sessions).
- **Multi-Device Support:** Tokens work across devices (web, mobile, desktop) without server-side session coupling.
- **Automatic Token Refresh:** Better Auth SDK handles refresh token flow transparently, improving UX (no forced re-login every 15 minutes).
- **XSS Protection:** httpOnly cookies prevent JavaScript access to tokens, mitigating XSS attack vectors.
- **Password Security:** bcrypt with 12 rounds is resistant to brute-force attacks (computational cost ~250ms per hash, acceptable for auth flows).
- **Middleware Integration:** FastAPI dependency injection allows clean `get_current_user` middleware applied to protected routes.
- **Token Expiry Balance:** 15-minute access tokens limit compromise window, 7-day refresh tokens balance security and UX (users don't re-login daily).
- **Framework-Agnostic:** Better Auth SDK works with FastAPI backend and Next.js frontend without tight coupling to framework internals.
- **User Isolation Enforcement:** JWT middleware extracts `user_id`, enforcing data isolation at API layer before database queries execute.

### Negative

- **Shared Secret Management:** Both frontend and backend MUST have identical BETTER_AUTH_SECRET environment variable (misconfiguration breaks authentication).
- **Token Revocation Complexity:** JWTs are stateless, making immediate revocation difficult (access tokens remain valid until 15-minute expiry, even after logout).
- **Cookie-Based Limitations:** httpOnly cookies don't work for cross-origin requests without proper CORS configuration (requires CORS_ORIGINS=http://localhost:3000 in backend .env).
- **Refresh Token Storage:** Refresh tokens in httpOnly cookies are still vulnerable to CSRF attacks (mitigated by SameSite cookie attribute in production).
- **Better Auth SDK Lock-In:** Switching to alternative auth library (e.g., Auth0, Clerk) requires rewriting auth service layer and frontend integration.
- **Token Size Overhead:** JWTs are larger than session IDs (base64-encoded header + payload + signature), adding ~200 bytes per request.
- **Clock Skew Sensitivity:** JWT expiration checks rely on server clock accuracy (NTP drift can cause false token expirations).

## Alternatives Considered

### Alternative Architecture A: Session-Based Auth with Redis
- **Components:** Server-side sessions stored in Redis, session ID in httpOnly cookie, bcrypt password hashing, no JWT
- **Pros:** Immediate session revocation (delete from Redis), smaller cookie size (32-byte session ID), no token refresh complexity, easier to audit active sessions.
- **Cons:** Requires Redis infrastructure (added complexity), stateful API (requires sticky sessions or session replication), Redis adds single point of failure (requires HA setup), doesn't scale as easily to mobile apps (requires session sync).
- **Why Rejected:** Stateful architecture complicates horizontal scaling, Redis adds infrastructure complexity for Phase II, session-based auth less suited for future mobile apps (Phase V).

### Alternative Architecture B: OAuth 2.0 with Third-Party Provider (Auth0, Clerk)
- **Components:** OAuth 2.0 flow, third-party provider handles authentication, backend verifies provider-issued tokens, no password storage
- **Pros:** No password storage (security outsourced), social login support (Google, GitHub), managed security updates, no bcrypt hashing needed.
- **Cons:** Vendor lock-in to provider, costs money at scale (Clerk charges per MAU), requires internet connection for auth (offline mode impossible), users must trust third-party, adds network latency (token verification API calls).
- **Why Rejected:** Vendor lock-in and cost not justified for Phase II scope, team wants full control over authentication flow, offline-first use cases may be needed in future phases.

### Alternative Architecture C: Passwordless Auth (Magic Links via Email)
- **Components:** Email-based magic links (one-time login tokens), no passwords, JWT tokens after email verification, SendGrid/Mailgun for email delivery
- **Pros:** No password storage (eliminates password security concerns), better UX for users (no password to remember), no bcrypt hashing needed.
- **Cons:** Requires email infrastructure (SendGrid/Mailgun), users without email access locked out, email delivery delays (3-10 seconds), email spam filters can block magic links, adds email sending cost.
- **Why Rejected:** Email infrastructure complexity not justified for Phase II, spec explicitly requires password-based signup/login (FR-001, FR-002), magic links increase latency in login flow.

## References

- Feature Spec: `specs/002-fullstack-web-auth/spec.md` (FR-001 to FR-006 for auth requirements, SC-001 to SC-003 for password complexity)
- Implementation Plan: `specs/002-fullstack-web-auth/plan.md` (Constraints: "All protected routes MUST verify JWT")
- Research: `specs/002-fullstack-web-auth/research.md` (Section 1: Better Auth Integration, Section 6: Password Validation)
- Data Model: `specs/002-fullstack-web-auth/data-model.md` (User model with password_hash field, Task model with user_id foreign key)
- Related ADRs: ADR-0001 (Frontend Stack uses Better Auth React SDK), ADR-0002 (Backend Stack uses Better Auth Python SDK), ADR-0004 (Database enforces user_id filtering)
- OpenAPI Contract: `specs/002-fullstack-web-auth/contracts/openapi.yaml` (BearerAuth security scheme, /api/auth/* endpoints)
- Constitution: `.specify/memory/constitution.md` (Principle VII: Security mandates AuthN/AuthZ and data isolation)
