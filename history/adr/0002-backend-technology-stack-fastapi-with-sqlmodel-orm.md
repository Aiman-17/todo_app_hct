# ADR-0002: Backend Technology Stack - FastAPI with SQLModel ORM

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Backend Stack" not separate ADRs for framework, ORM, server).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 002-fullstack-web-auth
- **Context:** Phase II migrates from in-memory console storage to a production-grade backend with database persistence, RESTful API, and JWT authentication. Backend must enforce user isolation at the data layer and provide type-safe database operations.

## Decision

**Adopt Python 3.13+ with FastAPI, Uvicorn, SQLModel ORM, and Better Auth Python SDK as the integrated backend technology stack.**

Stack Components:
- **Language:** Python 3.13+ (latest stable with performance improvements)
- **Web Framework:** FastAPI 0.109+ (async REST API framework with OpenAPI auto-generation)
- **ASGI Server:** Uvicorn with standard extras (asynchronous server for FastAPI)
- **ORM:** SQLModel 0.0.14+ (MANDATORY - combines Pydantic validation + SQLAlchemy ORM)
- **Authentication:** Better Auth Python SDK (JWT token generation/verification)
- **Password Hashing:** bcrypt 4.1+ (industry-standard password hashing with 12 salt rounds)
- **Validation:** Pydantic 2.5+ with email validation (EmailStr)
- **Database Driver:** psycopg2-binary 2.9+ (PostgreSQL adapter)
- **Environment Config:** python-dotenv 1.0+ (load .env files)
- **Testing:** pytest (unit/integration tests)

## Consequences

### Positive

- **Type Safety:** SQLModel provides end-to-end type checking from database models to API schemas (Pydantic-based), catching errors at development time.
- **Auto-Generated OpenAPI Docs:** FastAPI automatically generates OpenAPI 3.0.3 spec and Swagger UI at `/docs` based on Pydantic schemas, reducing documentation maintenance.
- **Async Performance:** FastAPI + Uvicorn support async/await for concurrent request handling, improving performance under load.
- **Single Schema Definition:** SQLModel models define both database schema (SQLAlchemy) and API schema (Pydantic), eliminating duplication and keeping validation logic DRY.
- **SQL Injection Protection:** SQLModel parameterized queries prevent SQL injection attacks (no raw SQL allowed per constraint).
- **Developer Experience:** FastAPI provides excellent error messages, hot reload with `--reload`, and dependency injection for clean service layer patterns.
- **Migration Path from Phase I:** Phase I already uses Python for console app, allowing team to reuse Task model patterns and service layer logic.
- **JWT Integration:** Better Auth SDK provides standardized JWT token creation/verification aligned with frontend, ensuring consistent authentication flow.
- **APIRouter Domain Grouping:** FastAPI's APIRouter allows logical separation of auth endpoints (/api/auth/*) and task endpoints (/api/tasks/*), supporting future domain expansion.

### Negative

- **SQLModel Maturity:** SQLModel is relatively new (0.0.x versions) compared to mature ORMs like Django ORM or SQLAlchemy Core, potentially encountering edge case bugs.
- **Python Performance:** Python is slower than compiled languages (Go, Rust), though async FastAPI mitigates this for I/O-bound operations (database queries, API calls).
- **ORM Abstraction Overhead:** SQLModel adds abstraction layer over raw SQL, which can make complex queries harder to optimize (though composite indexes mitigate this for common queries).
- **Dependency Weight:** Better Auth SDK + bcrypt + psycopg2 + SQLModel create a moderately heavy dependency footprint compared to lightweight frameworks like Flask.
- **Raw SQL Ban:** MANDATORY SQLModel usage forbids raw SQL optimizations for edge cases (tradeoff for security and type safety).

## Alternatives Considered

### Alternative Stack A: Flask + SQLAlchemy Core + PyJWT
- **Components:** Flask 3.x (micro web framework), SQLAlchemy Core (SQL toolkit without ORM), PyJWT (JWT library), bcrypt, psycopg2
- **Pros:** Lightweight, mature ecosystem, full SQL control with SQLAlchemy Core, PyJWT is widely used for JWT handling.
- **Cons:** No automatic OpenAPI generation (requires manual documentation), no Pydantic validation (requires manual schema validation), SQLAlchemy Core requires writing raw SQL or query builders (loses type safety), no dependency injection pattern.
- **Why Rejected:** Lack of type safety (no Pydantic integration), manual OpenAPI documentation increases maintenance burden, Flask lacks async support (blocks during database queries).

### Alternative Stack B: Django REST Framework + Django ORM + djangorestframework-simplejwt
- **Components:** Django 5.x (batteries-included framework), Django ORM, Django REST Framework (DRF serializers/viewsets), simplejwt (JWT for DRF)
- **Pros:** Mature ecosystem, built-in admin panel, ORM with migrations, DRF provides standardized API patterns.
- **Cons:** Heavy framework (includes features not needed like templating, sessions, CSRF), Django ORM lacks Pydantic validation (uses Django Forms/Serializers), slower than async frameworks, opinionated structure (tight coupling to Django conventions).
- **Why Rejected:** Framework bloat for API-only backend (templating/admin panel unused), lack of async support for concurrent requests, Django ORM doesn't integrate with Pydantic (requires duplicate schema definitions in DRF serializers).

### Alternative Stack C: Node.js + Express + Prisma ORM + bcryptjs
- **Components:** Node.js 20+, Express 4.x (web framework), Prisma ORM (type-safe ORM for TypeScript), bcryptjs (password hashing), jsonwebtoken (JWT)
- **Pros:** Same language as frontend (TypeScript), Prisma provides excellent type safety, large npm ecosystem, async by default.
- **Cons:** Team lacks Node.js backend experience (primarily Python team), Prisma requires separate schema.prisma file (extra DSL to learn), Express lacks built-in validation (requires manual middleware like Joi), no automatic OpenAPI generation without additional libraries.
- **Why Rejected:** Team familiarity with Python (faster development velocity), FastAPI's auto-generated OpenAPI is superior to Express manual documentation, Pydantic validation is more Pythonic than Joi/Zod middleware.

## References

- Feature Spec: `specs/002-fullstack-web-auth/spec.md` (Technology Stack section mandates FastAPI + SQLModel)
- Implementation Plan: `specs/002-fullstack-web-auth/plan.md` (Technical Context section, Project Structure backend/)
- Research: `specs/002-fullstack-web-auth/research.md` (Section 2: SQLModel Best Practices, Section 1: Better Auth Integration)
- Data Model: `specs/002-fullstack-web-auth/data-model.md` (SQLModel class definitions for User and Task models)
- Related ADRs: ADR-0003 (Authentication Architecture), ADR-0004 (Database Architecture - SQLModel pooling config)
- OpenAPI Contract: `specs/002-fullstack-web-auth/contracts/openapi.yaml` (defines 11 endpoints this stack implements)
- Constitution: `.specify/memory/constitution.md` (Principle V: Quality & Compliance emphasizes testable code)
