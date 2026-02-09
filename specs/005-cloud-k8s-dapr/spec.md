# Feature Specification: Cloud Kubernetes Deployment with Dapr & Kafka

**Feature Branch**: `005-cloud-k8s-dapr`
**Created**: 2026-02-07
**Status**: Planned (Phase 4 Complete)
**Input**: Phase 5 — Deploy to production-grade Kubernetes (GKE/DOKS/AKS/OKE), integrate Redpanda Cloud for Kafka, implement full Dapr stack (Pub/Sub, State, Bindings, Secrets, Service Invocation), add advanced features (Recurring Tasks, Due Dates, Reminders), and set up CI/CD pipeline.

---

## Overview

Phase 5 extends the local Kubernetes deployment (Phase 4) to **production-grade cloud infrastructure** with:
- **Cloud Kubernetes**: Deploy to GKE, DOKS, AKS, or Oracle Cloud (OKE)
- **Managed Kafka**: Use Redpanda Cloud (serverless, free tier) for event streaming
- **Full Dapr Stack**: Pub/Sub, State Management, Cron Bindings, Secrets, Service Invocation
- **Advanced Features**: Recurring tasks, due date reminders, priorities, tags, search, filters
- **Event-Driven Architecture**: Real-time notifications, audit logs, multi-client sync
- **CI/CD Pipeline**: Automated testing, building, and deployment via GitHub Actions
- **Observability**: Monitoring, logging, and distributed tracing

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Deploy to Cloud Kubernetes (Priority: P1)

A developer runs a deployment script that provisions a production Kubernetes cluster on GKE/DOKS/AKS/OKE, pushes Docker images to a cloud container registry, and deploys the application via Helm. The application is accessible via a public URL with HTTPS enabled.

**Why this priority**: Cloud deployment is the foundation of Phase 5. It proves the application is production-ready and can scale beyond local development.

**Independent Test**: Run deployment script, wait for pods to be Ready, access the public URL, perform login and task operations, verify HTTPS certificate is valid.

**Acceptance Scenarios**:

1. **Given** valid cloud credentials, **When** the deployment script runs, **Then** a Kubernetes cluster is provisioned within 10 minutes.
2. **Given** the cluster is ready, **When** images are pushed and Helm is installed, **Then** all pods reach Ready state within 5 minutes.
3. **Given** the application is deployed, **When** a user accesses the public URL, **Then** the application loads with a valid HTTPS certificate.

---

### User Story 2 — Event-Driven Task Reminders with Kafka & Dapr (Priority: P2)

When a user creates a task with a due date, the backend publishes a `reminder.scheduled` event to Kafka (via Dapr Pub/Sub). A separate notification service (or Dapr Cron Binding) consumes this event and sends a reminder notification at the appropriate time.

**Why this priority**: Event-driven reminders demonstrate the full Kafka + Dapr integration and deliver real user value (automated task notifications).

**Independent Test**: Create a task with due date "in 5 minutes", wait for notification service to consume the event, verify notification is triggered at the correct time.

**Acceptance Scenarios**:

1. **Given** a task with a due date, **When** the task is created, **Then** a `reminder.scheduled` event is published to Kafka topic `todo.reminders`.
2. **Given** the notification service is subscribed to `todo.reminders`, **When** the due time is reached, **Then** a notification is sent to the user (email/push/webhook).
3. **Given** a task is deleted before its due date, **When** a `reminder.cancelled` event is published, **Then** the notification service cancels the scheduled reminder.

---

### User Story 3 — Recurring Tasks Engine (Priority: P3)

When a user marks a recurring task as complete (e.g., "Pay rent" - Monthly), the backend publishes a `task.completed` event. A recurring task service consumes this event and automatically creates the next occurrence with the updated due date.

**Why this priority**: Recurring tasks are a key advanced feature that differentiates the app from basic todo lists. Kafka enables decoupled, scalable implementation.

**Independent Test**: Create a recurring task (Daily), mark it complete, verify a new instance is automatically created with tomorrow's due date.

**Acceptance Scenarios**:

1. **Given** a task with recurrence rule "Daily", **When** the task is marked complete, **Then** a new task is created with due date = current due date + 1 day.
2. **Given** a task with recurrence rule "Weekly", **When** completed, **Then** a new task is created with due date = current due date + 7 days.
3. **Given** a recurring task is deleted, **When** marked complete, **Then** no new occurrence is created (recurrence ends).

---

### User Story 4 — Real-Time Sync Across Clients (Priority: P4)

When a task is created, updated, or deleted from one client (web, mobile, CLI), all other connected clients receive a real-time update via WebSocket. Changes appear instantly without requiring a manual refresh.

**Why this priority**: Real-time sync is essential for multi-device productivity apps and demonstrates Kafka's ability to broadcast events to multiple consumers.

**Independent Test**: Open the app in two browser tabs, create a task in Tab 1, verify it appears in Tab 2 within 2 seconds without refresh.

**Acceptance Scenarios**:

1. **Given** two clients connected via WebSocket, **When** a task is created in Client A, **Then** Client B receives the update within 2 seconds.
2. **Given** multiple clients, **When** a task is updated (title, priority, due date), **Then** all clients reflect the change in real-time.
3. **Given** a client is offline, **When** reconnected, **Then** the client receives all missed updates (event replay from Kafka).

---

### User Story 5 — CI/CD Pipeline with GitHub Actions (Priority: P5)

When a developer pushes code to the `main` branch, GitHub Actions automatically runs tests, builds Docker images, pushes them to the container registry, and deploys the latest version to the staging environment. Production deployment requires manual approval.

**Why this priority**: CI/CD is essential for maintaining code quality and enabling rapid iteration in production.

**Independent Test**: Push a commit to `main`, verify GitHub Actions workflow runs, check staging environment receives the update within 10 minutes.

**Acceptance Scenarios**:

1. **Given** a commit is pushed to `main`, **When** GitHub Actions runs, **Then** all tests must pass (unit, integration, E2E).
2. **Given** tests pass, **When** Docker images are built, **Then** images are tagged with commit SHA and pushed to the registry.
3. **Given** images are pushed, **When** Helm upgrade runs, **Then** staging environment is updated within 5 minutes with zero downtime.

---

### Edge Cases

- **Kafka broker unavailable**: Task operations complete synchronously via database; events queue locally and replay when Kafka reconnects (Dapr resiliency).
- **Cloud provider outage**: Application continues serving traffic from healthy replicas; monitoring alerts DevOps team; auto-healing kicks in.
- **Database connection loss**: Backend retries with exponential backoff; user sees "Service temporarily unavailable" message; operations resume when connection restored.
- **CI/CD pipeline failure**: Deployment halts at failed step; previous version continues running; alerts sent to DevOps; no user impact.
- **WebSocket connection drops**: Frontend automatically reconnects with exponential backoff; fetches missed updates via REST API; seamless user experience.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Cloud Infrastructure
- **FR-001**: The application MUST be deployable to at least one cloud Kubernetes provider (GKE, DOKS, AKS, or Oracle Cloud OKE).
- **FR-002**: Docker images MUST be stored in a cloud container registry (GCR, DOCR, ACR, or OCIR) accessible to the Kubernetes cluster.
- **FR-003**: The application MUST be accessible via a public URL with HTTPS enabled (using Let's Encrypt or cloud-managed certificates).
- **FR-004**: All environment-specific configuration MUST be externalized (ConfigMaps, Secrets) to support multiple environments (dev, staging, production).

#### Kafka Integration
- **FR-005**: The application MUST connect to Redpanda Cloud (or equivalent managed Kafka) for event streaming.
- **FR-006**: The following Kafka topics MUST be created and used:
  - `todo.tasks.created` - Task creation events
  - `todo.tasks.updated` - Task update events
  - `todo.tasks.completed` - Task completion events
  - `todo.tasks.deleted` - Task deletion events
  - `todo.reminders.scheduled` - Reminder scheduling events
  - `todo.reminders.triggered` - Reminder notification events
  - `todo.sync.updates` - Real-time client sync events
- **FR-007**: All task CRUD operations MUST publish corresponding events to Kafka with the schema defined in `contracts/kafka-events.schema.md`.

#### Dapr Full Stack
- **FR-008**: Dapr MUST be deployed to the cloud Kubernetes cluster with all sidecars injected automatically.
- **FR-009**: **Pub/Sub Component**: MUST connect to Redpanda Cloud for event publishing and subscription.
- **FR-010**: **State Store Component**: MUST use PostgreSQL (Neon) for distributed state management.
- **FR-011**: **Cron Binding Component**: MUST trigger reminder checks every 5 minutes via Dapr input bindings.
- **FR-012**: **Secrets Component**: MUST integrate with Kubernetes Secrets for secure credential management.
- **FR-013**: **Service Invocation**: MUST use Dapr service-to-service calls with built-in retries and circuit breakers.

#### Advanced Features
- **FR-014**: Users MUST be able to create recurring tasks with the following recurrence rules:
  - Daily (repeat every N days)
  - Weekly (repeat every N weeks)
  - Monthly (repeat every N months)
  - Yearly (repeat every N years)
- **FR-015**: Users MUST be able to set due dates and receive reminders at configurable intervals (e.g., 1 day before, 1 hour before).
- **FR-016**: Users MUST be able to assign priorities (High, Medium, Low) to tasks.
- **FR-017**: Users MUST be able to add tags to tasks for categorization.
- **FR-018**: Users MUST be able to search tasks by title, description, or tags with real-time results.
- **FR-019**: Users MUST be able to filter tasks by priority, status, due date range, and tags.
- **FR-020**: Users MUST be able to sort tasks by created date, due date, priority, or last updated.

#### CI/CD Pipeline
- **FR-021**: A GitHub Actions workflow MUST run on every push to `main` branch with the following stages:
  - Lint and type-check (ESLint, TypeScript, mypy)
  - Run unit tests (backend + frontend)
  - Run integration tests (API endpoints)
  - Build Docker images
  - Push images to container registry
  - Deploy to staging environment
  - Run smoke tests against staging
- **FR-022**: Production deployment MUST require manual approval via GitHub Actions protected environment.
- **FR-023**: CI/CD pipeline MUST fail-fast: if any stage fails, subsequent stages do not run.

#### Observability
- **FR-024**: All services MUST emit structured logs (JSON format) with correlation IDs for distributed tracing.
- **FR-025**: All services MUST expose Prometheus-compatible metrics at `/metrics` endpoint.
- **FR-026**: The application MUST integrate with a logging aggregator (e.g., Cloud Logging, Elasticsearch) for centralized log management.
- **FR-027**: Critical alerts (pod crash, high error rate, latency > 5s) MUST trigger notifications via email or Slack.

---

### Non-Functional Requirements

#### Performance
- **NFR-001**: API response time MUST be < 500ms at p95 under normal load (100 concurrent users).
- **NFR-002**: Event publishing to Kafka MUST not block API requests (async processing).
- **NFR-003**: Real-time updates MUST propagate to all clients within 2 seconds.
- **NFR-004**: The application MUST support auto-scaling (2-10 replicas) based on CPU/memory usage.

#### Reliability
- **NFR-005**: The application MUST achieve 99.5% uptime in production (measured monthly).
- **NFR-006**: Zero-downtime deployments MUST be supported via rolling updates with health checks.
- **NFR-007**: Database connection failures MUST trigger exponential backoff retries (max 3 attempts).
- **NFR-008**: Kafka connection failures MUST not cause task operations to fail (graceful degradation).

#### Security
- **NFR-009**: All external traffic MUST use HTTPS with valid TLS certificates.
- **NFR-010**: Database credentials and API keys MUST be stored as Kubernetes Secrets (never in source code).
- **NFR-011**: Container images MUST be scanned for vulnerabilities (critical/high CVEs blocked).
- **NFR-012**: Network policies MUST restrict pod-to-pod communication to only necessary paths.

#### Scalability
- **NFR-013**: The application MUST handle 1000 concurrent users without degradation.
- **NFR-014**: Kafka topics MUST support message retention of 7 days.
- **NFR-015**: The database MUST support connection pooling (min 10, max 100 connections).

#### Maintainability
- **NFR-016**: All infrastructure MUST be defined as code (Terraform/Helm, no manual console changes).
- **NFR-017**: Deployment rollback MUST complete within 5 minutes via `helm rollback`.
- **NFR-018**: Documentation MUST include runbooks for common operational tasks (scaling, troubleshooting, disaster recovery).

---

## Kafka Event Schemas

### Task Event Schema
```json
{
  "event_type": "created | updated | completed | deleted",
  "task_id": "integer",
  "task_data": {
    "id": "integer",
    "title": "string",
    "description": "string | null",
    "priority": "high | medium | low | null",
    "due_at": "ISO 8601 datetime | null",
    "tags": ["string"],
    "recurrence_rule": "string | null",
    "completed": "boolean",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  },
  "user_id": "string",
  "timestamp": "ISO 8601 datetime",
  "correlation_id": "UUID"
}
```

### Reminder Event Schema
```json
{
  "event_type": "scheduled | triggered | cancelled",
  "task_id": "integer",
  "title": "string",
  "due_at": "ISO 8601 datetime",
  "remind_at": "ISO 8601 datetime",
  "user_id": "string",
  "timestamp": "ISO 8601 datetime",
  "correlation_id": "UUID"
}
```

---

## Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                        CLOUD KUBERNETES CLUSTER (GKE/DOKS/AKS/OKE)           │
│                                                                               │
│  ┌─────────────────────────┐        ┌─────────────────────────────────────┐ │
│  │  Frontend (Next.js)     │        │  Backend (FastAPI)                  │ │
│  │  - 2-5 replicas         │◀──────▶│  - 3-10 replicas                    │ │
│  │  - Dapr Sidecar         │        │  - Dapr Sidecar                     │ │
│  │  - Auto-scaling (HPA)   │        │  - Auto-scaling (HPA)               │ │
│  │  - Health checks        │        │  - Health checks                    │ │
│  └──────────┬──────────────┘        └──────────┬──────────────────────────┘ │
│             │                                    │                            │
│             │                                    │                            │
│  ┌──────────▼────────────────────────────────────▼──────────────────────┐   │
│  │                     DAPR COMPONENTS                                   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ pubsub.kafka     │  │ state.postgresql │  │ bindings.cron    │   │   │
│  │  │ (Redpanda Cloud) │  │ (Neon DB)        │  │ (Reminders)      │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                         │   │
│  │  │ secretstores.k8s │  │ Service Invoke   │                         │   │
│  │  │ (API Keys, Creds)│  │ (mTLS)           │                         │   │
│  │  └──────────────────┘  └──────────────────┘                         │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│             │                                    │                            │
│             │                                    │                            │
│  ┌──────────▼────────────────────────────────────▼──────────────────────┐   │
│  │  Microservices (Event Consumers)                                     │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ Notification Svc │  │ Recurring Task   │  │ Audit Service    │   │   │
│  │  │ (Reminders)      │  │ Engine           │  │ (Activity Log)   │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Redpanda Cloud     │  │  Neon PostgreSQL    │  │  Cloud Logging      │
│  (Kafka)            │  │  (Database)         │  │  & Monitoring       │
│  - Serverless       │  │  - Serverless       │  │  - Prometheus       │
│  - 7-day retention  │  │  - Connection pool  │  │  - Grafana          │
│  - Multi-region     │  │  - Auto-scaling     │  │  - Alerting         │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

---

## Implementation Roadmap

### Phase 5A: Cloud Infrastructure Setup
- [ ] Provision cloud Kubernetes cluster (GKE/DOKS/AKS/OKE)
- [ ] Set up cloud container registry
- [ ] Configure cloud networking (VPC, subnets, firewall rules)
- [ ] Set up HTTPS ingress with TLS certificates
- [ ] Deploy Dapr to cloud cluster

### Phase 5B: Kafka & Dapr Integration
- [ ] Create Redpanda Cloud cluster (free serverless tier)
- [ ] Configure Dapr Pub/Sub component for Redpanda
- [ ] Implement event publishing for task CRUD operations
- [ ] Set up Dapr State Store (PostgreSQL)
- [ ] Configure Dapr Secrets Management
- [ ] Implement Dapr Service Invocation

### Phase 5C: Advanced Features
- [ ] Implement recurring tasks (data model + UI + backend logic)
- [ ] Implement due dates and reminders (Dapr Cron Binding)
- [ ] Add priorities and tags (database schema + UI)
- [ ] Implement advanced search (full-text search)
- [ ] Implement filters and sorting (query optimization)
- [ ] Build notification service (email/push/webhook)
- [ ] Implement recurring task engine (Kafka consumer)
- [ ] Add real-time sync (WebSocket + Kafka events)

### Phase 5D: CI/CD Pipeline
- [ ] Create GitHub Actions workflow for main branch
- [ ] Add linting and type-checking stages
- [ ] Add unit test stage (backend + frontend)
- [ ] Add integration test stage
- [ ] Add Docker build and push stage
- [ ] Add Helm deployment stage (staging)
- [ ] Add smoke test stage
- [ ] Configure production deployment with manual approval

### Phase 5E: Observability
- [ ] Implement structured logging with correlation IDs
- [ ] Add Prometheus metrics endpoints
- [ ] Set up Grafana dashboards
- [ ] Configure alerting rules (Slack/email)
- [ ] Implement distributed tracing (OpenTelemetry)

---

## Success Criteria

Phase 5 is considered complete when:
- ✅ Application is deployed to a cloud Kubernetes provider with public HTTPS URL
- ✅ Redpanda Cloud is integrated for Kafka event streaming
- ✅ Full Dapr stack is operational (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- ✅ All advanced features are implemented (recurring tasks, reminders, priorities, tags, search, filters)
- ✅ CI/CD pipeline deploys automatically to staging on `main` commits
- ✅ Application handles 1000 concurrent users with < 500ms p95 latency
- ✅ 99.5% uptime achieved in production
- ✅ Zero-downtime deployments validated
- ✅ Comprehensive documentation (runbooks, architecture diagrams, setup guides)

---

## Dependencies

- **Phase 4 (Complete)**: Minikube deployment, Helm charts, Dockerfiles
- **External Services**:
  - Cloud provider account with free credits:
    - **Google Cloud (GKE)**: $300 credits for 90 days
    - **DigitalOcean (DOKS)**: $200 credits for 60 days
    - **Azure (AKS)**: $200 credits for 30 days
    - **Oracle Cloud (OKE)**: $300 credits for 30 days + Always Free tier
  - Redpanda Cloud account (free serverless tier)
  - Neon PostgreSQL (already in use)
  - GitHub Actions (free for public repos)
- **Tools**:
  - kubectl, Helm, Docker (already installed in Codespaces)
  - Cloud CLI (gcloud/doctl/az/oci)
  - Dapr CLI

---

## Documentation

- [Plan](plan.md) - Implementation strategy and architecture decisions
- [Tasks](tasks.md) - Task breakdown with dependencies
- [Quickstart](quickstart.md) - 30-minute cloud deployment guide
- [Contracts](contracts/) - API schemas, Kafka event formats, Dapr component configs
- [Research](research.md) - Technology evaluation and trade-offs

---

## Notes

- **Free Credits Available**: All major cloud providers offer free credits for new accounts (see Dependencies section for amounts and durations).
- **Cost Optimization**: Use auto-scaling to minimize costs during low traffic; scale down staging environments when not in use; delete resources after hackathon to avoid charges.
- **Hackathon Timeline**: Prioritize P1 and P2 user stories for core functionality; P3-P5 can be implemented post-submission.
- **Future Work**: After hackathon, consider adding mobile app, voice commands for reminders, AI-powered task prioritization, and team collaboration features.
