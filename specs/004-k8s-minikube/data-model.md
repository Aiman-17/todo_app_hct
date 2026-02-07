# Data Model: Phase 4 — Deployment Topology

**Branch**: `004-k8s-minikube` | **Date**: 2026-02-03
**Purpose**: Define all entities, their attributes, relationships, and state transitions for Phase 4 infrastructure.

---

## Entity Diagram (Logical)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Minikube Cluster                             │
│                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────────────┐  │
│  │  Backend Pod │   │ Frontend Pod │   │  Dapr Control Plane    │  │
│  │  + Dapr      │   │  + Dapr      │   │  (dapr-system ns)      │  │
│  │    Sidecar   │   │    Sidecar   │   └────────────────────────┘  │
│  └──────┬───────┘   └──────┬───────┘                               │
│         │                  │                                        │
│         ▼                  ▼                                        │
│  ┌──────────────┐   ┌──────────────┐                               │
│  │ Dapr Pub/Sub │   │ Dapr State   │                               │
│  │ (Kafka)      │   │ Store (Redis)│                               │
│  └──────┬───────┘   └──────────────┘                               │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐   │
│  │ Kafka Broker │   │ Redis        │   │ Kagent               │   │
│  │ (Bitnami)    │   │ (Bitnami)    │   │ (kagent ns)          │   │
│  └──────────────┘   └──────────────┘   └──────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Ingress (nginx)  →  routes / to Frontend, /api/* to Backend │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                          │  (network)
                          ▼
                  ┌───────────────┐
                  │ Neon PostgreSQL│  (external — unchanged from Phase III)
                  └───────────────┘
```

---

## Entities

### 1. Container Image — Backend

| Attribute | Value |
|-----------|-------|
| Name | `todo-backend` |
| Base | `python:3.13-slim` |
| Port | 8000 |
| Entrypoint | `uvicorn src.main:app --host 0.0.0.0 --port 8000` |
| Build context | `backend/` |
| Secrets consumed | `DATABASE_URL`, `BETTER_AUTH_SECRET`, `GEMINI_API_KEY` |

### 2. Container Image — Frontend

| Attribute | Value |
|-----------|-------|
| Name | `todo-frontend` |
| Base | `node:20-alpine` (multi-stage: build → production) |
| Port | 3000 |
| Entrypoint | `next start` |
| Build context | `frontend/` |
| Env at runtime | `NEXT_PUBLIC_API_URL` (points to backend via Dapr or ClusterIP) |

### 3. Helm Chart — `todo-app`

| Attribute | Value |
|-----------|-------|
| Chart name | `todo-app` |
| Location | `charts/todo-app/` |
| Sub-charts | `bitnami/kafka`, `bitnami/redis` (via `requirements.yaml` / `Chart.lock`) |
| Namespaces | `ai-taskmaster` (app), `dapr-system` (Dapr), `kagent` (Kagent) |
| Key templates | `backend-deployment`, `frontend-deployment`, `ingress`, `dapr-pubsub`, `dapr-statestore`, `secrets`, `configmap` |

### 4. Dapr Component — Pub/Sub (Kafka)

| Attribute | Value |
|-----------|-------|
| Kind | `Component` (Dapr CRD) |
| Type | `dapr.io/v1alpha1` |
| Name | `todo-pubsub` |
| Backing | Kafka broker at `kafka.ai-taskmaster.svc.cluster.local:9092` |
| Namespace | `ai-taskmaster` |

### 5. Dapr Component — State Store (Redis)

| Attribute | Value |
|-----------|-------|
| Kind | `Component` (Dapr CRD) |
| Type | `dapr.io/v1alpha1` |
| Name | `todo-statestore` |
| Backing | Redis at `redis.ai-taskmaster.svc.cluster.local:6379` |
| Namespace | `ai-taskmaster` |

### 6. Kafka Topics

| Topic Name | Published By | Event Payload |
|------------|--------------|---------------|
| `todo.tasks.created` | Backend (ActionAgent → MCP add_task) | `{ task_id, title, user_id, created_at }` |
| `todo.tasks.updated` | Backend (ActionAgent → MCP update_task) | `{ task_id, changes, user_id, updated_at }` |
| `todo.tasks.completed` | Backend (ActionAgent → MCP complete_task) | `{ task_id, completed, user_id, updated_at }` |
| `todo.tasks.deleted` | Backend (ActionAgent → MCP delete_task) | `{ task_id, user_id, deleted_at }` |

### 7. Ingress

| Attribute | Value |
|-----------|-------|
| Controller | nginx (Minikube addon) |
| Host | `localhost` (Minikube tunnel) |
| `/` | → `frontend-service:3000` |
| `/api/*` | → `backend-service:8000` |
| TLS | Disabled for Minikube (re-enabled in Phase 5) |

---

## State Transitions

### Pod Lifecycle
```
Image Built → Pending → Running (Ready) → Healthy
                  ↑                            │
                  │         CrashLoopBackOff ←─┘ (auto-restart)
                  └── Pending (resource exhaustion)
```

### Kafka Event Flow
```
User Action (UI / Chatbot)
    → Backend receives request
    → MCP tool executes DB operation (sync, always succeeds)
    → Backend publishes event to Dapr pub/sub (async, best-effort)
        → Dapr sidecar forwards to Kafka broker
        → Event available on topic for consumers
    → Response returned to user
```

---

## Validation Rules

- Backend container MUST start and bind port 8000 within 30 seconds.
- Frontend container MUST serve a valid HTTP response on port 3000 within 30 seconds.
- Kafka topics MUST be auto-created on first publish (Kafka `auto.create.topics.enable=true`).
- Dapr sidecars MUST be injected (verify via `kubectl get pods -o yaml | grep daprd`).
- No secret value may appear in any Helm template file; all secrets use `{{ .Values.secrets.* }}` with values provided at install time or via a sealed-secrets mechanism.
