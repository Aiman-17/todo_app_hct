# Implementation Plan: Cloud Kubernetes Deployment with Dapr & Kafka

**Branch**: `005-cloud-k8s-dapr` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-cloud-k8s-dapr/spec.md`

## Summary

Phase 5 extends the local Kubernetes deployment (Phase 4) to production-grade cloud infrastructure. The primary requirement is to deploy the AI TaskMaster application to a cloud Kubernetes provider (GKE/DOKS/AKS/OKE) with full event-driven architecture using Dapr and Kafka (Redpanda Cloud). This includes implementing advanced features (recurring tasks, reminders, priorities, tags, search), setting up CI/CD pipelines, and adding comprehensive observability.

**Technical Approach**: Build upon existing Minikube Helm charts (Phase 4), migrate to cloud container registry, integrate Redpanda Cloud for managed Kafka, deploy full Dapr stack with 5 components (Pub/Sub, State, Bindings, Secrets, Service Invocation), implement 3 microservices (Notification, Recurring Task Engine, Audit Service) as Kafka consumers, add GitHub Actions CI/CD workflow, and configure cloud-native monitoring/logging.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+ (FastAPI)
- Frontend: Node.js 20 LTS (Next.js 16, React 19)
- Infrastructure: YAML (Kubernetes manifests, Helm charts, Dapr components)

**Primary Dependencies**:
- **Kubernetes**: Cloud-managed cluster (GKE/DOKS/AKS/OKE)
- **Dapr**: 1.13+ (distributed application runtime)
- **Kafka**: Redpanda Cloud (serverless, free tier)
- **Container Registry**: GCR/DOCR/ACR/OCIR (cloud-managed)
- **Database**: Neon PostgreSQL (existing, unchanged)
- **CI/CD**: GitHub Actions
- **Backend**: FastAPI, SQLModel, psycopg, httpx, python-kafka
- **Frontend**: Next.js, React, WebSocket client, axios

**Storage**:
- **Primary Database**: Neon PostgreSQL (existing)
- **State Store**: PostgreSQL via Dapr State Management component
- **Event Store**: Kafka topics on Redpanda Cloud (7-day retention)
- **Container Images**: Cloud container registry (GCR/DOCR/ACR/OCIR)

**Testing**:
- **Backend**: pytest, pytest-asyncio, httpx (test client)
- **Frontend**: Jest, React Testing Library
- **Integration**: Kafka test containers, Dapr sidecar mock
- **E2E**: Playwright or Cypress
- **Performance**: k6 or Locust (load testing)

**Target Platform**:
- **Primary**: Cloud Kubernetes (GKE Autopilot / DOKS / AKS / OKE)
- **Development**: GitHub Codespaces + Minikube (Phase 4 validated)
- **CI/CD**: GitHub Actions runners

**Performance Goals**:
- API p95 latency < 500ms under 100 concurrent users
- Event publishing to Kafka: async, non-blocking (< 50ms overhead)
- Real-time sync propagation < 2 seconds
- Zero-downtime deployments (rolling updates)
- Auto-scaling 2-10 replicas based on CPU/memory

**Constraints**:
- **Budget**: Use free credits (GKE $300, DOKS $200, AKS $200, OKE $300)
- **Phase Isolation**: Phase 2/3 code is FROZEN (read-only, no modifications)
- **Dapr Requirement**: All inter-service communication via Dapr APIs (no direct HTTP)
- **Event-First**: All task operations MUST publish Kafka events
- **Security**: No hardcoded secrets, HTTPS required, container vulnerability scans

**Scale/Scope**:
- **Users**: 1000 concurrent users (target capacity)
- **Events**: 10k events/day initially, scalable to 1M/day
- **Microservices**: 6 services (frontend, backend, notification, recurring-task, audit, websocket)
- **Kafka Topics**: 7 topics (tasks.created/updated/completed/deleted, reminders.scheduled/triggered, sync.updates)
- **Deployment Environments**: 3 (dev, staging, production)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Spec-First Development
- **Status**: PASS
- **Evidence**: Complete spec.md exists at `specs/005-cloud-k8s-dapr/spec.md` with 5 user stories, 27 functional requirements, NFRs, and success criteria.
- **Action**: None required.

### ✅ Principle II: Agent-Centric Workflow
- **Status**: PASS
- **Evidence**: This plan will be executed through specialized agents (deployment-orchestrator, dapr-config-manager, kafka-event-manager, kubernetes-operator).
- **Action**: None required.

### ✅ Principle III: Skill Reusability
- **Status**: PASS
- **Evidence**: Reusing existing skills (deploy, k8s-deploy, containerize) and creating new skills for Dapr/Kafka operations.
- **Action**: Create new skills for Phase 5:
  - `dapr-config.skill.md` - Dapr component configuration
  - `kafka-events.skill.md` - Kafka event publishing/consuming
  - `cloud-deploy.skill.md` - Cloud K8s deployment workflow

### ✅ Principle IV: Phase-Based Evolution
- **Status**: PASS with CRITICAL CONSTRAINTS
- **Evidence**: Phase 4 (Minikube) is complete and validated. Phase 5 extends to cloud.
- **Constraints (MANDATORY)**:
  - **Phase 2/3 Code is FROZEN**: No modifications to existing backend/frontend code
  - **Additive-only changes**: New microservices (notification, recurring-task, audit) are NEW services
  - **Read-reuse-reference**: New services MAY call Phase 2 APIs, read Phase 2 models, but NEVER MODIFY
  - **Explicit exceptions**: ANY modification to Phase 2/3 requires TodoMasterAgent approval + ADR
- **Action**: Document in ADR if any Phase 2/3 modification is attempted.

### ✅ Principle V: Quality & Compliance
- **Status**: PASS
- **Evidence**: CI/CD pipeline includes:
  - Unit tests (backend + frontend)
  - Integration tests (API contracts, Kafka events)
  - E2E tests (full user workflows)
  - Code coverage thresholds (80%+)
  - SpecAgent validation before deployment
- **Action**: None required.

### ✅ Principle VI: Event-Driven Architecture
- **Status**: PASS (CORE REQUIREMENT)
- **Evidence**:
  - All task CRUD operations publish Kafka events
  - 3 event-driven microservices (Notification, Recurring Task Engine, Audit)
  - Dapr Pub/Sub abstracts Kafka complexity
  - Event schemas defined in contracts/
- **Action**: None required.

###⚠️ Principle VII: Security
- **Status**: REQUIRES ATTENTION
- **Evidence**: Phase 2/3 has JWT auth, HTTPS, secrets management
- **Required for Phase 5**:
  - Kubernetes Secrets for all credentials (no hardcoded values)
  - Network policies for pod isolation
  - Container vulnerability scanning in CI/CD
  - mTLS via Dapr Service Invocation
  - HTTPS ingress with TLS certificates (Let's Encrypt or cloud-managed)
- **Action**: Add security checks to CI/CD pipeline (Trivy scan, Secrets detection).

---

## Project Structure

### Documentation (this feature)

```text
specs/005-cloud-k8s-dapr/
├── spec.md              # ✅ Complete (already created)
├── plan.md              # 📄 This file
├── research.md          # 🔄 Phase 0 output (to be created)
├── data-model.md        # 🔄 Phase 1 output (to be created)
├── quickstart.md        # 🔄 Phase 1 output (to be created)
├── contracts/           # 🔄 Phase 1 output (to be created)
│   ├── kafka-events.schema.json
│   ├── dapr-pubsub.yaml
│   ├── dapr-statestore.yaml
│   ├── dapr-bindings.yaml
│   ├── dapr-secrets.yaml
│   └── notification-api.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Existing Structure (Phase 2/3/4 - FROZEN, READ-ONLY)
backend/                              # ❌ FROZEN (Phase 2/3)
├── src/
│   ├── models/                       # ✅ Can READ (Task, User models)
│   ├── services/                     # ✅ Can CALL (TaskService, AuthService)
│   ├── api/                          # ✅ Can CALL (REST endpoints)
│   └── agents/                       # ✅ Can CALL (chatbot agents)
└── tests/

frontend/                             # ❌ FROZEN (Phase 2/3)
├── src/
│   ├── components/                   # ✅ Can READ (UI components)
│   ├── app/                          # ✅ Can CALL (pages, API routes)
│   └── services/                     # ✅ Can CALL (API client)
└── tests/

charts/todo-app/                      # ⚠️ EXTENDS (Phase 4 → Phase 5)
├── templates/
│   ├── backend-deployment.yaml       # ✅ Can MODIFY (add Dapr annotations)
│   ├── frontend-deployment.yaml      # ✅ Can MODIFY (add Dapr annotations)
│   ├── dapr-pubsub.yaml              # ➕ NEW (Kafka Pub/Sub component)
│   ├── dapr-statestore.yaml          # ➕ NEW (PostgreSQL state store)
│   ├── dapr-bindings.yaml            # ➕ NEW (Cron binding for reminders)
│   ├── dapr-secrets.yaml             # ➕ NEW (Kubernetes secrets)
│   ├── notification-deployment.yaml  # ➕ NEW (Notification service)
│   ├── recurring-task-deployment.yaml # ➕ NEW (Recurring task engine)
│   ├── audit-deployment.yaml         # ➕ NEW (Audit service)
│   └── websocket-deployment.yaml     # ➕ NEW (WebSocket sync service)
└── values.yaml                       # ✅ Can MODIFY (add new services)

# New Structure (Phase 5 - ADDITIVE ONLY)
services/                             # ➕ NEW DIRECTORY
├── notification/                     # ➕ NEW SERVICE
│   ├── src/
│   │   ├── main.py                   # Entry point
│   │   ├── kafka_consumer.py         # Subscribe to reminders.scheduled
│   │   ├── notifier.py               # Email/push/webhook sender
│   │   └── config.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── recurring-task/                   # ➕ NEW SERVICE
│   ├── src/
│   │   ├── main.py                   # Entry point
│   │   ├── kafka_consumer.py         # Subscribe to tasks.completed
│   │   ├── task_generator.py         # Create next occurrence
│   │   └── recurrence_rules.py       # Parse RRULE strings
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── audit/                            # ➕ NEW SERVICE
│   ├── src/
│   │   ├── main.py                   # Entry point
│   │   ├── kafka_consumer.py         # Subscribe to all task events
│   │   ├── audit_log.py              # Store activity log
│   │   └── query_api.py              # Audit log query endpoints
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
└── websocket/                        # ➕ NEW SERVICE
    ├── src/
    │   ├── main.py                   # FastAPI WebSocket server
    │   ├── kafka_consumer.py         # Subscribe to sync.updates
    │   ├── connection_manager.py     # Manage WebSocket connections
    │   └── broadcaster.py            # Broadcast to connected clients
    ├── tests/
    ├── requirements.txt
    └── Dockerfile

.github/                              # ➕ NEW DIRECTORY
└── workflows/
    ├── ci.yml                        # Lint, test, build
    ├── cd-staging.yml                # Deploy to staging (auto)
    └── cd-production.yml             # Deploy to production (manual approval)

deploy/                               # ⚠️ EXTENDS (Phase 4 → Phase 5)
├── values.secret.yaml                # ✅ Can MODIFY (add Kafka credentials)
├── cloud/                            # ➕ NEW (cloud-specific configs)
│   ├── gke/
│   │   ├── cluster-config.yaml
│   │   └── ingress-tls.yaml
│   ├── doks/
│   │   ├── cluster-config.yaml
│   │   └── ingress-tls.yaml
│   └── aks/
│       ├── cluster-config.yaml
│       └── ingress-tls.yaml
└── scripts/                          # ➕ NEW (deployment automation)
    ├── deploy-to-gke.sh
    ├── deploy-to-doks.sh
    ├── deploy-to-aks.sh
    └── setup-dapr.sh
```

**Structure Decision**:

Phase 5 adopts a **microservices architecture** with additive-only changes:
1. **Existing services (backend/frontend)** remain unchanged at the code level (FROZEN)
2. **New microservices (services/)** are created as independent services
3. **Helm charts** are extended with Dapr components and new service deployments
4. **CI/CD pipelines** are added as new workflows
5. **Cloud configs** are isolated in deploy/cloud/ per provider

This structure satisfies Phase Isolation Rules:
- ✅ No modifications to Phase 2/3 code
- ✅ New services are truly NEW (not refactors)
- ✅ Communication via Dapr Service Invocation (not direct HTTP)
- ✅ Event-driven decoupling via Kafka

---

## Complexity Tracking

### Violations Requiring Justification

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 6 services total (backend, frontend, notification, recurring-task, audit, websocket) | Event-driven architecture requires decoupled, independently scalable services. Notification and recurring-task are CPU-intensive background jobs that should not block the main API. | Combining into 1-2 monoliths would couple business logic, increase deployment risk, and make horizontal scaling impossible for specific workloads (e.g., scale notification service independently during high load). |
| Dapr abstraction layer | Provides service mesh features (mTLS, retries, circuit breakers, secrets management, pub/sub) without code changes. Required for cloud-native resilience. | Direct Kafka client code would couple application logic to Kafka SDK, increase boilerplate, and miss built-in resilience patterns. Switching from Kafka to RabbitMQ would require code changes across 6 services instead of 1 YAML change. |
| Separate Kafka topics per event type (7 topics) | Enables fine-grained consumer subscriptions (notification service only needs reminders, audit service needs all events). Follows event-driven best practices. | Single topic would require all consumers to filter messages at runtime, increasing network bandwidth, processing overhead, and coupling (changing task events would break unrelated consumers). |
| 3 deployment environments (dev, staging, production) | Required for safe rollouts: dev for feature development, staging for integration testing, production for live traffic. Manual approval gate between staging and production prevents accidental deployments. | 2 environments (dev, production) would skip integration testing phase, increasing risk of production incidents. 1 environment (production only) is unacceptable for any production system. |

---

## Phase 0: Research & Technology Evaluation

### Objectives
- Resolve all "NEEDS CLARIFICATION" items from Technical Context
- Evaluate cloud providers (GKE vs DOKS vs AKS vs OKE)
- Evaluate Kafka providers (Redpanda Cloud vs Confluent Cloud vs self-hosted)
- Determine Dapr component configurations
- Define event schemas and contracts
- Research WebSocket scaling patterns for real-time sync

### Research Tasks

1. **Cloud Provider Evaluation**
   - **Question**: Which cloud provider offers best Kubernetes experience within free credit budget?
   - **Evaluation Criteria**:
     - Kubernetes API compatibility (all should be 100% compatible)
     - Free credits amount and duration
     - Ease of setup (CLI, web console)
     - Auto-scaling capabilities (HPA support)
     - Load balancer / Ingress costs
     - Container registry pricing
   - **Output**: Decision matrix with recommendation

2. **Managed Kafka Evaluation**
   - **Question**: Which Kafka provider offers best free tier for event-driven architecture?
   - **Evaluation Criteria**:
     - Free tier limits (throughput, retention, topics)
     - Ease of setup (managed vs self-hosted)
     - Dapr compatibility (official connector support)
     - Multi-region availability
     - Latency (producer → consumer)
   - **Output**: Decision matrix with recommendation (likely Redpanda Cloud due to generous free tier)

3. **Dapr Component Configuration Research**
   - **Question**: How to configure each of the 5 Dapr components for production?
   - **Components**:
     - Pub/Sub (Kafka): Connection strings, authentication, topic creation
     - State Store (PostgreSQL): Connection pooling, transaction isolation
     - Cron Binding: Schedule syntax, timezone handling
     - Secrets (Kubernetes): Secret rotation, access control
     - Service Invocation: mTLS, retries, timeouts
   - **Output**: Example YAML configurations for each component

4. **Event Schema Design**
   - **Question**: What should the Kafka event schema look like for task operations?
   - **Requirements**:
     - JSON schema for task events (created, updated, completed, deleted)
     - JSON schema for reminder events (scheduled, triggered, cancelled)
     - JSON schema for sync events (real-time updates)
     - Versioning strategy (schema evolution)
     - Correlation IDs for distributed tracing
   - **Output**: JSON schemas in contracts/

5. **WebSocket Scaling Research**
   - **Question**: How to scale WebSocket service horizontally with Kafka pub/sub?
   - **Challenges**:
     - Sticky sessions (client must reconnect to same pod)
     - Broadcast to all connected clients (across pods)
     - Connection state management
     - Graceful shutdown during deployments
   - **Output**: Architecture diagram and implementation strategy

6. **CI/CD Pipeline Design**
   - **Question**: What should the GitHub Actions workflow include for cloud deployments?
   - **Stages**:
     - Lint and type-check (Python, TypeScript)
     - Unit tests (backend, frontend, microservices)
     - Integration tests (API contracts, Kafka events)
     - E2E tests (Playwright)
     - Docker build and push (all 6 services)
     - Helm deployment (staging auto, production manual)
     - Smoke tests (health checks, basic workflows)
   - **Output**: Workflow YAML templates

### Deliverable: research.md

Structure:
```markdown
# Phase 5 Research Report

## 1. Cloud Provider Comparison
[Decision matrix, selected provider, rationale]

## 2. Managed Kafka Comparison
[Decision matrix, selected provider (Redpanda Cloud), rationale]

## 3. Dapr Component Configurations
[Example YAMLs for all 5 components with annotations]

## 4. Event Schemas
[Links to contracts/ with JSON schemas]

## 5. WebSocket Scaling Architecture
[Architecture diagram, connection management strategy]

## 6. CI/CD Pipeline Design
[Workflow stages, deployment strategy, approval gates]

## 7. Security Considerations
[Secrets management, network policies, vulnerability scanning]

## 8. Cost Estimation
[Resource usage, free credit burn rate, scalability costs]
```

---

## Phase 1: Design & Contracts

### Objectives
- Define data models for new entities (RecurringTask, Reminder, AuditLog)
- Create API contracts for new microservices
- Document Dapr component YAMLs
- Create quickstart guide for cloud deployment
- Update agent context files

### Design Tasks

1. **Data Model Extension (data-model.md)**
   - Extend existing Task model with new fields:
     - `recurrence_rule` (string, nullable): RRULE format (RFC 5545)
     - `priority` (enum): high, medium, low, null
     - `tags` (array of strings)
     - `due_at` (datetime, nullable)
     - `remind_at` (datetime, nullable)
   - New entities:
     - **Reminder**: id, task_id, remind_at, status (pending, sent, cancelled), created_at
     - **AuditLog**: id, event_type, task_id, user_id, task_data (JSON), timestamp, correlation_id
   - Database migrations:
     - Alembic migration to add new Task fields
     - Create reminders table
     - Create audit_logs table

2. **API Contracts (contracts/)**
   - **Kafka Event Schemas**:
     - `task-event.schema.json` (created, updated, completed, deleted events)
     - `reminder-event.schema.json` (scheduled, triggered, cancelled events)
     - `sync-event.schema.json` (real-time sync updates)
   - **Dapr Component YAMLs**:
     - `dapr-pubsub.yaml` (Kafka Pub/Sub component)
     - `dapr-statestore.yaml` (PostgreSQL state store)
     - `dapr-bindings.yaml` (Cron binding for reminders)
     - `dapr-secrets.yaml` (Kubernetes secrets component)
   - **Microservice APIs**:
     - `notification-api.openapi.yaml` (webhook endpoints)
     - `audit-api.openapi.yaml` (query audit logs)
     - `websocket-api.md` (WebSocket protocol)

3. **Quickstart Guide (quickstart.md)**
   - Prerequisites (cloud account, CLI tools)
   - Step 1: Provision cloud Kubernetes cluster
   - Step 2: Install Dapr on cluster
   - Step 3: Configure Redpanda Cloud (Kafka)
   - Step 4: Build and push Docker images
   - Step 5: Create Kubernetes secrets
   - Step 6: Deploy via Helm
   - Step 7: Verify deployment (health checks, logs)
   - Step 8: Test event-driven workflows
   - Troubleshooting common issues

4. **Agent Context Update**
   - Run: `.specify/scripts/bash/update-agent-context.sh claude`
   - Add new technologies:
     - Dapr 1.13+ (distributed application runtime)
     - Redpanda Cloud (managed Kafka)
     - GitHub Actions (CI/CD)
   - Preserve manual additions

### Deliverables
- `data-model.md` - Extended Task model, new entities, migrations
- `contracts/` - Event schemas, Dapr YAMLs, API specs
- `quickstart.md` - 30-minute cloud deployment guide
- Agent context file updated

---

## Phase 2: Implementation Roadmap

**NOTE**: This is NOT the tasks.md file. This is a high-level implementation roadmap. The `/sp.tasks` command will generate the detailed task breakdown.

### Phase 5A: Cloud Infrastructure Setup (P1 - CRITICAL PATH)
- Provision cloud Kubernetes cluster (GKE/DOKS/AKS/OKE)
- Set up cloud container registry (GCR/DOCR/ACR/OCIR)
- Configure HTTPS ingress with TLS certificates (Let's Encrypt or cloud-managed)
- Deploy Dapr to cloud cluster (dapr init -k)
- Configure network policies for pod isolation

### Phase 5B: Kafka & Dapr Integration (P1 - CRITICAL PATH)
- Create Redpanda Cloud cluster (free serverless tier)
- Create Kafka topics (7 topics as per FR-006)
- Configure Dapr Pub/Sub component (connect to Redpanda)
- Implement event publishing in backend (task CRUD operations)
- Configure Dapr State Store (PostgreSQL)
- Configure Dapr Secrets Management (Kubernetes Secrets)
- Implement Dapr Service Invocation (backend → frontend communication)

### Phase 5C: Microservices Development (P2 - PARALLEL TRACK)
- **Notification Service**:
  - Kafka consumer subscribing to `reminders.scheduled`
  - Email/push/webhook sender (configurable)
  - Dapr Cron Binding integration
  - Health check endpoints
- **Recurring Task Engine**:
  - Kafka consumer subscribing to `tasks.completed`
  - RRULE parser (RFC 5545)
  - Task generator (create next occurrence)
  - Dapr Service Invocation to backend API
- **Audit Service**:
  - Kafka consumer subscribing to all task events
  - Audit log storage (PostgreSQL)
  - Query API (filter by user, event type, date range)
- **WebSocket Service**:
  - Kafka consumer subscribing to `sync.updates`
  - WebSocket connection manager
  - Broadcaster (push to all connected clients)
  - Graceful shutdown on deployment

### Phase 5D: Advanced Features (P3 - ADDITIVE WORK)
- **Recurring Tasks**:
  - UI: Recurrence rule selector (Daily, Weekly, Monthly, Yearly)
  - Backend: RRULE validation and storage
  - Event publishing on task completion
- **Due Dates & Reminders**:
  - UI: Date picker, reminder interval selector
  - Backend: Store due_at and remind_at
  - Dapr Cron Binding triggers reminder checks every 5 minutes
- **Priorities & Tags**:
  - UI: Priority dropdown (High, Medium, Low), tag input
  - Backend: Store priority and tags array
  - Search/filter by priority and tags
- **Advanced Search**:
  - Backend: PostgreSQL full-text search on title/description
  - UI: Search input with debounce (300ms)
  - Filter by priority, status, due date range, tags
  - Sort by created_at, due_at, priority, updated_at

### Phase 5E: CI/CD Pipeline (P4 - AUTOMATION)
- Create GitHub Actions workflow for main branch:
  - Stage 1: Lint (ESLint, black, mypy)
  - Stage 2: Unit tests (backend + frontend + microservices)
  - Stage 3: Integration tests (API contracts, Kafka events)
  - Stage 4: Docker build and push (6 services, tagged with commit SHA)
  - Stage 5: Helm upgrade to staging (auto-deploy)
  - Stage 6: Smoke tests (health checks, basic workflows)
- Create production deployment workflow:
  - Manual approval required
  - Helm upgrade to production
  - Post-deployment verification
- Configure branch protection rules (require tests to pass)

### Phase 5F: Observability (P5 - PRODUCTION READINESS)
- Implement structured logging with correlation IDs (all services)
- Add Prometheus metrics endpoints (/metrics)
- Set up Grafana dashboards (traffic, latency, error rates)
- Configure alerting rules (Slack/email notifications)
- Implement distributed tracing (OpenTelemetry)
- Set up log aggregation (Cloud Logging or Elasticsearch)

---

## Dependencies

### Phase 4 Completion (MANDATORY)
- ✅ Minikube deployment working
- ✅ Helm charts created
- ✅ Docker images for backend/frontend
- ✅ Kubernetes manifests validated

### External Services
- Cloud provider account (GKE/DOKS/AKS/OKE) with free credits
- Redpanda Cloud account (free serverless tier)
- GitHub repository (for Actions CI/CD)
- Domain name (optional, for HTTPS ingress)

### Tools
- kubectl (installed in Codespaces)
- Helm 3.16+ (installed in Codespaces)
- Docker (installed in Codespaces)
- Cloud CLI (gcloud/doctl/az/oci - to be installed)
- Dapr CLI (to be installed)

---

## Success Criteria

Phase 5 is considered complete when:
- ✅ Application deployed to cloud Kubernetes with public HTTPS URL
- ✅ All 6 services running (backend, frontend, notification, recurring-task, audit, websocket)
- ✅ Redpanda Cloud integrated, all 7 Kafka topics created
- ✅ Full Dapr stack operational (5 components configured)
- ✅ Event-driven workflows validated:
  - Task operations publish Kafka events
  - Reminders triggered by Dapr Cron Binding
  - Recurring tasks auto-created after completion
  - Real-time sync working across clients
- ✅ CI/CD pipeline deploying to staging automatically
- ✅ Advanced features implemented (priorities, tags, search, filters)
- ✅ Performance goals met (p95 < 500ms, sync < 2s)
- ✅ Zero-downtime deployment validated (rolling updates)
- ✅ Documentation complete (runbooks, quickstart, contracts)

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Free credit exhaustion before completion | Medium | High | Monitor spending daily, use auto-scaling to minimize costs, scale down non-prod environments |
| Kafka connection failures | Low | High | Implement Dapr resiliency (retries, circuit breakers), graceful degradation (task operations succeed even if event publishing fails) |
| WebSocket scaling complexity | Medium | Medium | Use sticky sessions (session affinity in ingress), implement connection state management with Redis if needed |
| Phase 2/3 code modification violations | High | Critical | Strict code review, automated checks in CI/CD, SpecAgent validation |
| CI/CD pipeline complexity | Medium | Medium | Start with minimal pipeline (lint + test + deploy), iterate incrementally |
| Cloud provider API differences | Low | Low | Use Helm charts (portable across K8s), avoid provider-specific features |

---

## Next Steps

1. **Execute Phase 0 Research** - Run research agents to resolve all NEEDS CLARIFICATION
2. **Review research.md** - User approval required before Phase 1
3. **Execute Phase 1 Design** - Generate data-model.md, contracts/, quickstart.md
4. **Re-check Constitution** - Validate no violations introduced during design
5. **Generate tasks.md** - Run `/sp.tasks` command to create detailed task breakdown
6. **Begin Implementation** - Start with Phase 5A (cloud infrastructure setup)

---

**Plan Status**: ✅ COMPLETE
**Next Command**: `/sp.tasks` (after research.md and data-model.md are validated)
