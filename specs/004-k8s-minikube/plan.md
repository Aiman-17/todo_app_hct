# Implementation Plan: Phase 4 — Local Kubernetes Deployment

**Branch**: `004-k8s-minikube` | **Date**: 2026-02-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/004-k8s-minikube/spec.md`

---

## Summary

Containerize the Todo Chatbot backend (FastAPI) and frontend (Next.js) using Docker (with Gordon AI assistance), package the full application stack as a Helm chart, and deploy to a local Minikube cluster. Integrate Dapr sidecars for Kafka pub/sub event publishing and Redis state store. Use kubectl-ai (Google) and Kagent for AI-assisted Kubernetes operations throughout. All Phase I/II/III source code remains frozen; Phase 4 adds only Dockerfiles, Helm chart, Dapr component YAMLs, and a deployment runbook.

---

## Technical Context

**Language/Version**: Python 3.13+ (backend), Node.js 20 LTS (frontend)
**Primary Dependencies**: FastAPI + Uvicorn (backend), Next.js 15 + React 18 (frontend), Helm 3, Dapr CLI, Minikube
**Storage**: Neon PostgreSQL (external, unchanged); Redis (in-cluster, Dapr state store); Kafka (in-cluster, Bitnami)
**Testing**: Container smoke tests (health probes), Helm lint (`helm lint`), event verification via Kafka console consumer
**Target Platform**: Minikube on Windows (Docker Desktop driver)
**Project Type**: Web application (backend + frontend) — Option 2
**Performance Goals**: All pods healthy within 2 min of deploy; full stack deploy < 5 min
**Constraints**: Minikube single-node; memory budget ~4–6 GB; replicas = 1 for local dev
**Scale/Scope**: 2 container images, 1 Helm chart with 2 sub-charts (Kafka, Redis), 4 Dapr components, 1 Kagent installation

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I — Spec-First | spec.md exists before implementation | PASS | Created in `/sp.specify` |
| II — Agent-Centric | Tasks routed through DockerAgent, KubernetesAgent, DaprAgent, KafkaAgent | PASS | Hackathon tools: Gordon, kubectl-ai, Kagent |
| III — Skill Reusability | Common deploy ops as skills | PASS | Quickstart runbook covers repeatable steps |
| IV — Phase Evolution | Phase 4 after Phase 3; Phase 3 fully functional | PASS | Phase III working on Vercel; Docker confirmed |
| IV — Phase Isolation | Phase I/II/III code frozen; additive-only | PASS | Only new files: Dockerfiles, charts/, deploy/ |
| V — Quality & Compliance | Tests before deploy | PASS | Helm lint + health probes + event verification |
| VI — Event-Driven | Kafka pub/sub for async ops | PASS | 4 topics, Dapr pub/sub component |
| VII — Security | JWT auth, secrets externalized | PASS | All secrets via K8s Secrets; no hardcoded values |

**Post-design re-check**: All gates remain PASS after Phase 1 design. No violations detected.

---

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-minikube/
├── spec.md                         # Feature requirements (created)
├── plan.md                         # This file
├── research.md                     # Tool decisions + installation research (created)
├── data-model.md                   # Deployment topology + entity definitions (created)
├── quickstart.md                   # Step-by-step runbook (created)
├── contracts/
│   ├── helm-values.schema.md       # Helm values contract (created)
│   └── kafka-events.schema.md      # Kafka event CloudEvents schemas (created)
├── checklists/
│   └── requirements.md             # Spec quality checklist (created)
└── tasks.md                        # Task breakdown (next: /sp.tasks)
```

### Source Code (additions only)

```text
todo_app_hct/                       # repo root
├── backend/
│   └── Dockerfile                  # EXISTS — needs port fix (7860 → 8000) + Python 3.13
├── frontend/
│   └── Dockerfile                  # TO CREATE via Gordon
├── charts/
│   └── todo-app/                   # TO CREATE — Helm chart
│       ├── Chart.yaml
│       ├── values.yaml             # parameterised from contracts/helm-values.schema.md
│       ├── templates/
│       │   ├── backend-deployment.yaml
│       │   ├── frontend-deployment.yaml
│       │   ├── backend-service.yaml
│       │   ├── frontend-service.yaml
│       │   ├── ingress.yaml
│       │   ├── secrets.yaml
│       │   ├── configmap.yaml
│       │   ├── dapr-pubsub.yaml
│       │   └── dapr-statestore.yaml
│       └── requirements.yaml       # sub-chart deps: bitnami/kafka, bitnami/redis
├── deploy/
│   ├── values.secret.yaml          # GITIGNORED — secrets at deploy time
│   └── .gitignore                  # ensures secrets never commit
└── kubernetes/                     # existing raw manifests (reference only; migrated into Helm)
    ├── backend-deployment.yaml
    ├── frontend-deployment.yaml
    ├── ingress.yaml
    └── namespace.yaml
```

**Structure Decision**: Option 2 (Web application). The existing `kubernetes/` directory contains raw manifests that serve as the source of truth for pod specs, but the delivered artifacts are the Helm chart under `charts/todo-app/`. The raw manifests are retained as reference.

---

## Phase 0: Research — COMPLETE

All unknowns resolved. See [research.md](research.md).

**Resolved decisions**:
1. Gordon for Docker operations (available, enabled)
2. Minikube with Docker driver
3. Helm v3 for packaging
4. kubectl-ai (Google) with Gemini backend
5. Kagent via Helm into cluster
6. Dapr CLI for K8s init
7. Kafka via Bitnami chart
8. Redis via Bitnami chart
9. Nginx ingress (Minikube addon), TLS stripped for local

**Existing artifact issues catalogued** (5 fixes required, all in Phase 4 implementation).

---

## Phase 1: Design — COMPLETE

### Data Model
See [data-model.md](data-model.md).
- 7 entities defined: Backend Image, Frontend Image, Helm Chart, Dapr Pub/Sub, Dapr State Store, Kafka Topics (4), Ingress.
- Deployment topology diagram included.
- State transitions for pod lifecycle and Kafka event flow documented.

### Contracts
See [contracts/](contracts/):
- **helm-values.schema.md** — full `values.yaml` structure with SECRET markers and install-time examples.
- **kafka-events.schema.md** — CloudEvents v1.0 schemas for all 4 task lifecycle topics.

### Quickstart
See [quickstart.md](quickstart.md).
- 9-step runbook from "prerequisites confirmed" to "app running on Minikube".
- Covers Gordon, minikube, helm, kubectl-ai, dapr, kagent installation.
- Teardown and troubleshooting sections included.

---

## Installation Summary (What Needs to Be Installed)

The following table answers the hackathon question directly:

| Tool | Purpose | Install Method | Status |
|------|---------|----------------|--------|
| Docker Desktop 4.53+ | Container runtime | Already installed (4.55.0) | DONE |
| Gordon (Docker AI) | AI-assisted Dockerfiles | Enable in Docker Desktop → Beta | To enable |
| kubectl | K8s CLI | Already installed (v1.34.1) | DONE |
| Minikube | Local K8s cluster | `minikube-installer.exe` | To install |
| Helm v3 | Chart package manager | Download `helm.exe` | To install |
| kubectl-ai (Google) | AI K8s assistant | Download zip, add to PATH | To install |
| Dapr CLI | Dapr K8s init | Download zip, add to PATH | To install |
| Kagent | In-cluster AI agent | `helm install` into cluster | To install (after Minikube) |
| Kafka (Bitnami) | Event broker | Sub-chart in Helm deploy | Auto (Helm) |
| Redis (Bitnami) | State store | Sub-chart in Helm deploy | Auto (Helm) |

---

## Blueprints & Spec-Driven Deployment (Research Note)

The hackathon requirement asks: *"Can Spec-Driven Development be used for infrastructure automation?"*

**Answer: Yes.** The pattern demonstrated in this plan is:

1. **Spec** (`spec.md`) defines WHAT the deployment must achieve — user outcomes, not implementation steps.
2. **Research** (`research.md`) resolves HOW — tool choices, installation paths, architectural decisions.
3. **Data Model** (`data-model.md`) defines the deployment topology as entities with relationships — the "blueprint".
4. **Contracts** define the interfaces between components (Helm values = configuration contract; Kafka schemas = event contract).
5. **Quickstart** is the executable runbook derived directly from the above artifacts.
6. **Tasks** (`tasks.md`, generated by `/sp.tasks`) break this into individually testable, independently deliverable work items.

This is the **Blueprint pattern**: spec → research → data-model + contracts → runbook → tasks. Each artifact is a Claude Code Agent Skill output, making the entire pipeline reproducible and auditable.

---

## Next Steps

1. Run `/sp.tasks` to generate `tasks.md` — the actionable, dependency-ordered task list for Phase 4 implementation.
2. Execute tasks in order: tool installation → Gordon Dockerfiles → Helm chart → Dapr components → Kagent → verification.
