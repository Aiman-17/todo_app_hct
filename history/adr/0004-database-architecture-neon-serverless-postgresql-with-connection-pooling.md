# ADR-0004: Database Architecture - Neon Serverless PostgreSQL with Connection Pooling

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Database Architecture" not separate ADRs for database, pooling, indexing).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 002-fullstack-web-auth
- **Context:** Phase II migrates from in-memory storage to persistent database with multi-user support. Database must support user isolation, handle concurrent requests efficiently, and provide zero-setup local development experience. Future phases may require database branching for preview environments (Phase V).

## Decision

**Adopt Neon Serverless PostgreSQL with SQLModel connection pooling, composite indexes for query optimization, and mandatory user_id filtering on all queries.**

Architecture Components:
- **Database:** Neon Serverless PostgreSQL (managed PostgreSQL with instant provisioning, auto-scaling, and database branching)
- **ORM:** SQLModel (MANDATORY - see ADR-0002 for ORM decision)
- **Connection Pooling:** SQLModel engine with pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=3600
- **SSL/TLS:** Required (`?sslmode=require` in connection string)
- **Schema Management:** SQLModel.metadata.create_all() for Phase II (Alembic migrations in Phase III+)
- **Indexes:**
  - Users.email (UNIQUE index for fast login lookup)
  - Tasks.user_id (FK index for user isolation filtering)
  - Tasks.(user_id, completed, created_at DESC) (composite index for optimized default sort query)
- **User Isolation:** ALL queries MUST filter by `user_id` from JWT token (enforced in service layer)
- **Data Types:** UUID for users.id (PostgreSQL native), INTEGER for tasks.id (sequential), TIMESTAMP for timestamps (UTC)

## Consequences

### Positive

- **Zero-Setup Local Development:** Neon provides instant cloud database (no local Postgres installation needed), reducing onboarding friction for developers.
- **Auto-Scaling:** Neon automatically scales compute up/down based on load, handling traffic spikes without manual intervention.
- **Database Branching:** Neon supports git-like database branching (create preview databases from main branch), enabling safe feature testing in Phase V.
- **Connection Pooling Performance:** pool_size=5 + max_overflow=10 allows 15 concurrent connections, sufficient for local development and small production workloads.
- **Cold Start Mitigation:** pool_pre_ping=True verifies connections before use, handling Neon's serverless cold starts gracefully (1-2 second wake-up).
- **Composite Index Optimization:** (user_id, completed, created_at DESC) index enables PostgreSQL to execute default task query (incomplete first, newest first) using index-only scan.
- **User Isolation at Database Layer:** user_id filtering on all queries prevents cross-user data leakage, even if JWT middleware is bypassed.
- **Type Safety:** SQLModel UUID and INTEGER types map directly to PostgreSQL UUID and INTEGER, preventing type mismatch errors.
- **SSL Enforcement:** `sslmode=require` ensures all database connections are encrypted, protecting data in transit.

### Negative

- **Vendor Lock-In:** Neon-specific features (database branching, instant provisioning) create migration friction to self-hosted Postgres or RDS.
- **Serverless Cold Starts:** Idle databases take 1-2 seconds to wake up (mitigated by pool_pre_ping but adds initial request latency).
- **Connection Pool Limits:** 15 max connections (pool_size + max_overflow) may be insufficient for high-traffic production (requires upgrading Neon plan or tuning pool settings).
- **Limited Free Tier:** Neon free tier has storage and compute limits (500MB storage, 100 compute hours/month), requiring paid plan for production.
- **No Local Development Fallback:** If Neon API is down, local development is blocked (unlike local Postgres which runs offline).
- **Composite Index Maintenance:** Composite index must be updated if default sort order changes (e.g., adding priority field), requiring schema migration.
- **SQLModel.metadata.create_all() Limitations:** Auto-creating tables on startup doesn't support migrations (adding columns, changing constraints) - requires manual Alembic setup in Phase III.

## Alternatives Considered

### Alternative Architecture A: Local PostgreSQL with Docker Compose
- **Components:** PostgreSQL 16 in Docker container, SQLModel ORM, connection pooling, pgAdmin for GUI management
- **Pros:** Full offline development support, no vendor lock-in, free unlimited usage, familiar Docker setup, database GUI included.
- **Cons:** Requires Docker installation (setup friction), manual database backups, no auto-scaling, developers must manage database lifecycle (start/stop containers), no database branching feature.
- **Why Rejected:** Docker setup increases onboarding complexity for non-DevOps team members, Neon's database branching feature valuable for Phase V preview environments, zero-setup cloud database reduces local dependency burden.

### Alternative Architecture B: Amazon RDS PostgreSQL with PgBouncer
- **Components:** Amazon RDS Postgres (managed PostgreSQL), PgBouncer (connection pooler), SQLModel ORM, AWS VPC for networking
- **Pros:** Mature AWS ecosystem, PgBouncer provides advanced pooling (transaction pooling mode), RDS backups automated, no cold starts.
- **Cons:** Requires AWS account setup, RDS has fixed compute (no auto-scaling without manual intervention), more expensive than Neon free tier, PgBouncer adds infrastructure complexity, slower provisioning (15-30 minutes vs Neon's instant).
- **Why Rejected:** AWS setup complexity not justified for Phase II, fixed compute doesn't match serverless scaling benefits, Neon free tier reduces costs for MVP.

### Alternative Architecture C: Supabase PostgreSQL (Neon Competitor)
- **Components:** Supabase (managed Postgres with auto-generated REST API), SQLModel ORM, connection pooling, built-in auth (alternative to Better Auth)
- **Pros:** Auto-generated REST API reduces backend boilerplate, built-in authentication (Supabase Auth), database GUI, real-time subscriptions, generous free tier.
- **Cons:** Auto-generated API bypasses backend validation logic (violates spec constraint "Backend MUST use SQLModel"), Supabase Auth conflicts with Better Auth decision (ADR-0003), tighter vendor lock-in than Neon (Supabase-specific APIs).
- **Why Rejected:** Auto-generated API violates spec's mandate for explicit FastAPI backend with Pydantic validation, Supabase Auth creates conflict with Better Auth SDK decision, team wants full control over API layer.

## References

- Feature Spec: `specs/002-fullstack-web-auth/spec.md` (Technology Stack mandates "Neon Serverless PostgreSQL")
- Implementation Plan: `specs/002-fullstack-web-auth/plan.md` (Storage: "Neon Serverless PostgreSQL with connection pooling")
- Research: `specs/002-fullstack-web-auth/research.md` (Section 2: SQLModel Best Practices with Neon, Section 4: Neon PostgreSQL Connection)
- Data Model: `specs/002-fullstack-web-auth/data-model.md` (SQLModel class definitions, composite index rationale, critical query patterns)
- Related ADRs: ADR-0002 (Backend Stack with SQLModel ORM), ADR-0003 (Authentication enforces user_id filtering on queries)
- Quickstart Guide: `specs/002-fullstack-web-auth/quickstart.md` (Neon connection string setup, troubleshooting)
- Constitution: `.specify/memory/constitution.md` (Principle V: Quality & Compliance emphasizes performance goals)
