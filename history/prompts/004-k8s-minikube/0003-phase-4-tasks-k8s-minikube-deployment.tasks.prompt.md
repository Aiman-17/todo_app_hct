---
id: 0003
title: Phase 4 Tasks — K8s Minikube Deployment Task List
stage: tasks
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-k8s-minikube
branch: 004-k8s-minikube
user: ACS
command: /sp.tasks
labels: ["phase-4","kubernetes","minikube","helm","dapr","kafka","gordon","kubectl-ai","kagent","tasks","aiops"]
links:
  spec: specs/004-k8s-minikube/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-k8s-minikube/tasks.md
tests:
 - none (tasks phase — infrastructure verification steps are embedded in task descriptions)
---

## Prompt

/sp.tasks

## Response snapshot

Generated complete Phase 4 dependency-ordered task list (42 tasks across 7 phases):
- **Phase 1 (Setup)**: T001–T005 — parallel tool installations (Minikube, Helm, kubectl-ai, Dapr CLI) + directory scaffold
- **Phase 2 (Foundational)**: T006–T009 — Minikube start, namespace + Dapr label, Dapr init, Gordon enable
- **Phase 3 (US1 — Containerize)**: T010–T012 — Fix backend/Dockerfile (port 7860→8000, Python 3.12→3.13) via Gordon, create frontend/Dockerfile via Gordon, smoke-test both images locally
- **Phase 4 (US2 — Helm Deploy)**: T013–T026 — Chart.yaml, values.yaml (from helm-values.schema.md contract), 6 parallel template files (secrets, configmap, 2 deployments, 2 services), ingress, sub-chart dependencies, lint, deploy, end-to-end verify
- **Phase 5 (US3 — Kafka Events)**: T027–T031 — Dapr pub/sub component YAML, verify component registration, verify all 4 CloudEvents topics, test graceful degradation when broker is down
- **Phase 6 (US4 — State Store)**: T032–T035 — Dapr state store component YAML, verify registration, round-trip smoke test via Dapr HTTP API, verify persistence across pod restart
- **Phase 7 (Polish)**: T036–T042 — Kagent install + kubectl-ai check (parallel), then sequential SC verification (SC-001 through SC-006), final helm lint

Critical path documented. 6 parallel opportunity windows identified. Phase boundaries enforce commit checkpoints.

## Outcome

- ✅ Impact: Task list complete. 42 tasks mapped to 4 user stories, 13 FRs, 6 SCs. All design artifacts consumed (spec, plan, research, data-model, contracts, quickstart). Zero unresolved dependencies.
- 🧪 Tests: None — tasks phase. Verification steps are embedded in-task (health probes, helm lint, kafka-console-consumer, Dapr HTTP API smoke tests).
- 📁 Files: tasks.md
- 🔁 Next prompts: `/sp.implement` to begin executing tasks in order, starting with Phase 1 tool installations
- 🧠 Reflection: Mapped 5 existing artifact issues from research.md directly into T010 (backend Dockerfile) and T011 (frontend Dockerfile). Kept Phase 5 (US3) and Phase 6 (US4) partially parallel since dapr-statestore.yaml creation (T032) is file-independent from Kafka event verification (T029–T031). Kagent install placed in Polish phase because it has no dependency from other user stories — it's a cluster-level tool, not a prerequisite.

## Evaluation notes (flywheel)

- Failure modes observed: none — all tasks derive directly from design artifacts with no ambiguity
- Graders run and results (PASS/FAIL): Task-to-US traceability check — 42/42 tasks tagged with [USn] or phase label; FR coverage — all 13 FRs covered; SC coverage — all 6 SCs mapped to verification tasks T038–T041
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): run /sp.implement to begin Phase 1 tool installations; alternatively, manually execute T001–T005 in parallel terminals
