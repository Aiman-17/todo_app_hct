# Tasks: Phase 4 — Local Kubernetes Deployment (Minikube)

**Input**: Design documents from `specs/004-k8s-minikube/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Phase 4 validation is infrastructure-based (health probes, helm lint, event consumption). No unit/integration test files are generated — verification steps are documented in-task per quickstart.md.

**Organization**: Tasks are grouped by phase. Phase 1 (Setup) and Phase 2 (Foundational) are sequential prerequisites. Phases 3–6 map 1:1 to user stories US1–US4. Phase 7 is Polish / cross-cutting.

---

## Phase 1: Setup (Tool Installation & Project Structure)

**Purpose**: Install all missing tools and create the directory scaffold required by the Helm chart. All Phase 1 tasks are independent and can run in parallel once the developer has a terminal open.

- [ ] T001 [P] Install Minikube via `minikube-installer.exe` — verify with `minikube version` (see quickstart.md Step 1a)
- [ ] T002 [P] Install Helm v3 — download `helm-v3.16.0-windows-amd64.zip`, place `helm.exe` in PATH, verify with `helm version` (see quickstart.md Step 1b)
- [ ] T003 [P] Install kubectl-ai (Google) — download zip from `GoogleCloudPlatform/kubectl-ai` releases, extract to `C:\kubectl-ai`, add to PATH, set `GEMINI_API_KEY` env var, verify with `kubectl-ai --help` (see quickstart.md Step 1c)
- [ ] T004 [P] Install Dapr CLI — download `dapr_windows_amd64.zip`, extract, add to PATH, verify with `dapr version` (see quickstart.md Step 1d)
- [X] T005 [P] Create directory structure: `charts/todo-app/templates/`, `deploy/`, `deploy/.gitignore` (gitignore must contain `values.secret.yaml`) — per plan.md Project Structure

**Checkpoint**: All tools installed and verified. Directory scaffold in place. Proceed to Phase 2.

---

## Phase 2: Foundational (Minikube Cluster & Dapr Runtime)

**Purpose**: Bring up the Minikube cluster and install cluster-wide infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T006 Start Minikube with Docker driver: `minikube start --driver=docker --memory=4096 --cpus=2` — enable addons: `ingress`, `dashboard`, `metrics-server` — verify with `kubectl get nodes` (see quickstart.md Step 2)
- [ ] T007 Create namespace `ai-taskmaster` and label for Dapr injection: `kubectl create namespace ai-taskmaster && kubectl label namespace ai-taskmaster dapr.io/enabled=true`
- [ ] T008 Install Dapr on cluster: `dapr init -k` — verify all Dapr system pods Running: `kubectl get pods -n dapr-system` (see quickstart.md Step 3)
- [ ] T009 Enable Gordon in Docker Desktop: Settings → Beta features → toggle Docker AI on — verify with `docker ai "What can you do?"` (see quickstart.md Step 0)

**Checkpoint**: Minikube Running, namespace `ai-taskmaster` exists with Dapr label, Dapr system pods healthy, Gordon enabled. User story implementation can now begin.

---

## Phase 3: User Story 1 — Containerize and Run Services Locally (Priority: P1) 🎯 MVP

**Goal**: Produce working `todo-backend` and `todo-frontend` container images using Gordon. Fix all catalogued issues in `backend/Dockerfile` and create `frontend/Dockerfile` from scratch.

**Independent Test**: `docker build` both images with zero errors; start both containers with correct env vars; hit frontend in browser and confirm login + task creation works.

### Implementation for User Story 1

- [X] T010 [US1] Fix `backend/Dockerfile`: change base image to `python:3.13-slim`, change `EXPOSE` and CMD port from 7860 to 8000 — use Gordon: `docker ai "Review backend/Dockerfile and fix port and Python version issues"` — verify with `docker build -t todo-backend ./backend`
- [X] T011 [US1] Create `frontend/Dockerfile` via Gordon: `docker ai "Create a production multi-stage Dockerfile for the Next.js app in frontend/"` — target `node:20-alpine`, multi-stage (build → production), expose port 3000, entrypoint `next start` — verify with `docker build -t todo-frontend ./frontend`
- [ ] T012 [US1] Smoke-test both images locally: `docker run -d --name backend-test -p 8000:8000 -e DATABASE_URL=<neon-url> -e BETTER_AUTH_SECRET=<secret> -e GEMINI_API_KEY=<key> todo-backend` and `docker run -d --name frontend-test -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 todo-frontend` — confirm `curl http://localhost:8000/api/health` returns `{"status":"healthy"}` and `curl http://localhost:3000` returns HTTP 200 — clean up test containers after

**Checkpoint**: Both images build and run. Health check passes. All Phase III features verified via local containers. US1 complete.

---

## Phase 4: User Story 2 — Deploy Full Stack to Minikube via Helm (Priority: P2)

**Goal**: Create the `todo-app` Helm chart, wire all Kubernetes resources, and deploy the full stack with a single `helm install` command.

**Independent Test**: `helm install` succeeds, all pods reach Ready within 2 min, ingress URL serves the login page, full task workflow completes end-to-end.

### Implementation for User Story 2

- [X] T013 [US2] Create `charts/todo-app/Chart.yaml` — name: `todo-app`, version: `0.1.0`, appVersion: `1.0.0`, add Bitnami repo dependency declarations for `kafka` and `redis` sub-charts
- [X] T014 [US2] Create `charts/todo-app/values.yaml` — populate from `contracts/helm-values.schema.md`: backend/frontend image+port+resources+healthProbe+env, ingress (TLS disabled), secrets block (empty defaults), dapr config, kafka topics list, redis flag, kagent config
- [X] T015 [P] [US2] Create `charts/todo-app/templates/secrets.yaml` — Kubernetes Secret resource in namespace `ai-taskmaster`; values sourced exclusively from `{{ .Values.secrets.* }}` (databaseUrl, betterAuthSecret, geminiApiKey) — no hardcoded values
- [X] T016 [P] [US2] Create `charts/todo-app/templates/configmap.yaml` — non-secret env vars (CORS_ORIGINS, ENVIRONMENT, NEXT_PUBLIC_API_URL) parameterised from `.Values`
- [X] T017 [P] [US2] Create `charts/todo-app/templates/backend-deployment.yaml` — 1 replica, image from `.Values.backend.image`, port 8000, env from Secret + ConfigMap, Dapr annotations (`dapr.io/enabled`, `dapr.io/appId: todo-backend`), liveness+readiness probes at `/api/health` with initialDelay 15s / period 10s, resource requests/limits from `.Values.backend.resources`
- [X] T018 [P] [US2] Create `charts/todo-app/templates/frontend-deployment.yaml` — 1 replica, image from `.Values.frontend.image`, port 3000, env `NEXT_PUBLIC_API_URL` from ConfigMap, Dapr annotations (`dapr.io/appId: todo-frontend`), liveness+readiness probes at `/` with initialDelay 15s / period 10s, resource requests/limits from `.Values.frontend.resources`
- [X] T019 [P] [US2] Create `charts/todo-app/templates/backend-service.yaml` — ClusterIP Service targeting port 8000 in namespace `ai-taskmaster`
- [X] T020 [P] [US2] Create `charts/todo-app/templates/frontend-service.yaml` — ClusterIP Service targeting port 3000 in namespace `ai-taskmaster`
- [X] T021 [US2] Create `charts/todo-app/templates/ingress.yaml` — nginx ingress class, host `localhost`, path `/` → `frontend-service:3000`, path `/api/*` → `backend-service:8000` — TLS block conditionally rendered via `{{ if .Values.ingress.tls.enabled }}` (disabled for Minikube)
- [X] T022 [US2] Create `charts/todo-app/requirements.yaml` (or `Chart.yaml` dependencies block) — declare `bitnami/kafka` and `bitnami/redis` sub-charts; run `helm dependency update ./charts/todo-app`
- [X] T023 [US2] Create `deploy/values.secret.yaml` (example/template only — actual secrets filled at deploy time; file is gitignored) — document the three SECRET keys
- [ ] T024 [US2] Lint and validate: run `helm lint ./charts/todo-app` — resolve all warnings/errors
- [ ] T025 [US2] Deploy: `helm install todo-app ./charts/todo-app -f deploy/values.secret.yaml` — watch pods: `kubectl get pods -n ai-taskmaster -w` — wait for backend + frontend + kafka + redis pods all Ready
- [ ] T026 [US2] Verify end-to-end: run `minikube tunnel`, open `http://localhost/` in browser, log in, create a task via chatbot, confirm task persists — also verify `http://localhost/api/health` returns healthy

**Checkpoint**: Full stack deployed and operational on Minikube. US2 complete.

---

## Phase 5: User Story 3 — Event-Driven Task Operations via Dapr and Kafka (Priority: P3)

**Goal**: Wire the backend to publish task lifecycle events to Kafka through the Dapr pub/sub sidecar. Verify events appear on the correct topics.

**Independent Test**: Perform a task action through the UI/chatbot, then consume from the corresponding Kafka topic and observe the CloudEvents-formatted event.

### Implementation for User Story 3

- [X] T027 [US3] Create `charts/todo-app/templates/dapr-pubsub.yaml` — Dapr Component CRD: kind `Component`, type `dapr.io/v1alpha1`, name `todo-pubsub`, spec type `kafka`, metadata: brokerURL `kafka.ai-taskmaster.svc.cluster.local:9092` — namespace `ai-taskmaster`
- [ ] T028 [US3] Verify Dapr pub/sub component is registered: `kubectl get components -n ai-taskmaster` — confirm `todo-pubsub` shows type `kafka`
- [ ] T029 [US3] Verify event publishing: perform a task create action via the chatbot, then consume from topic `todo.tasks.created`: `kubectl exec -it <kafka-pod> -n ai-taskmaster -- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic todo.tasks.created --from-beginning` — confirm a CloudEvents v1.0 payload appears with correct `type`, `source`, `id`, `data.task_id`
- [ ] T030 [US3] Verify remaining event types: repeat step T029 for update (`todo.tasks.updated`), complete (`todo.tasks.completed`), and delete (`todo.tasks.deleted`) — one task action per topic
- [ ] T031 [US3] Verify graceful degradation: if Kafka broker is down (e.g., scale Kafka to 0 replicas temporarily), perform a task operation — confirm the operation succeeds (task persists in DB) and a warning appears in backend logs — scale Kafka back up

**Checkpoint**: All 4 Kafka topics receive correctly-shaped CloudEvents. Graceful fallback when broker is unavailable. US3 complete.

---

## Phase 6: User Story 4 — Dapr State Store Integration (Priority: P4)

**Goal**: Deploy and wire the Dapr state store (Redis-backed) so backend pods can read/write state via the Dapr state API.

**Independent Test**: From a backend pod, issue a Dapr state store `set` then `get` call and confirm the value round-trips. Restart the pod and confirm the value survives.

### Implementation for User Story 4

- [X] T032 [US4] Create `charts/todo-app/templates/dapr-statestore.yaml` — Dapr Component CRD: kind `Component`, type `dapr.io/v1alpha1`, name `todo-statestore`, spec type `redis`, metadata: host `redis.ai-taskmaster.svc.cluster.local:6379` — namespace `ai-taskmaster`
- [ ] T033 [US4] Verify state store component is registered: `kubectl get components -n ai-taskmaster` — confirm `todo-statestore` shows type `redis`
- [ ] T034 [US4] Smoke-test state store round-trip: from a backend pod shell (`kubectl exec -it <backend-pod> -n ai-taskmaster -- sh`), run `curl -X POST http://localhost:3500/v1.0/state/todo-statestore -H "Content-Type: application/json" -d '[{"key":"test-key","value":"hello-phase4"}]'` then `curl http://localhost:3500/v1.0/state/todo-statestore/test-key` — confirm response contains `hello-phase4`
- [ ] T035 [US4] Verify persistence: delete the backend pod (`kubectl delete pod <backend-pod> -n ai-taskmaster`), wait for restart, re-run the `get` from T034 — confirm value still returns (Redis-backed persistence)

**Checkpoint**: State store deployed, accessible, and persistent across pod restarts. US4 complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Install Kagent, run final verification against all success criteria, and ensure the deployment is clean and repeatable.

- [ ] T036 [P] Install Kagent: `helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds --namespace kagent --create-namespace` then `helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent --namespace kagent --set providers.openAI.apiKey=<key>` — open dashboard with `kagent dashboard` (see quickstart.md Step 6)
- [ ] T037 [P] Use kubectl-ai for cluster health check: `kubectl-ai "show me the pods in the ai-taskmaster namespace"` and `kubectl-ai "check cluster health"` — document output
- [ ] T038 Verify SC-001: deploy from scratch (helm uninstall → helm install) and confirm full stack is up in under 5 minutes
- [ ] T039 Verify SC-002: confirm all pods reach Ready within 2 minutes of helm install with zero manual intervention
- [ ] T040 Verify SC-005: clean teardown — `helm uninstall todo-app`, `helm uninstall kagent -n kagent`, `helm uninstall kagent-crds -n kagent`, `dapr uninstall -k`, `minikube stop` — confirm no leftover resources
- [X] T041 Verify SC-006: audit all files in `charts/todo-app/` — confirm zero hardcoded secrets; all sensitive values use `{{ .Values.secrets.* }}`
- [ ] T042 Final: run `helm lint ./charts/todo-app` one last time — all clean; update quickstart.md if any steps changed during implementation

**Checkpoint**: All 6 success criteria verified. Kagent operational. Deployment is clean, repeatable, and lint-free. Phase 4 complete.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — all T001–T005 can start immediately and run in parallel
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories. T006 must run before T007; T007 before T008
- **US1 — Containerize (Phase 3)**: Depends on Phase 2 (Gordon enabled via T009). T010 → T011 → T012 (sequential: backend first, then frontend, then smoke test)
- **US2 — Helm Deploy (Phase 4)**: Depends on Phase 3 (images must exist). T013+T014 first (Chart.yaml + values.yaml), then T015–T022 in parallel, then T022 → T023 → T024 → T025 → T026 (sequential)
- **US3 — Kafka Events (Phase 5)**: Depends on Phase 4 (full stack deployed). T027 → T028 → T029–T031
- **US4 — State Store (Phase 6)**: Depends on Phase 4 (cluster running). T032 can run in parallel with Phase 5 (different files, no shared state). T032 → T033 → T034 → T035
- **Polish (Phase 7)**: Depends on Phases 5 and 6 completion. T036+T037 can run in parallel; T038–T042 are sequential verification

### Parallel Opportunities

- **Phase 1**: T001, T002, T003, T004, T005 — all independent installs
- **Phase 4 (Helm templates)**: T015, T016, T017, T018, T019, T020 — all independent template files
- **Phase 6 vs Phase 5**: T032 (dapr-statestore.yaml) can be created while Phase 5 event verification is running
- **Phase 7**: T036 (Kagent install) and T037 (kubectl-ai check) are independent

### Critical Path

```
T001-T005 (parallel) → T006 → T007 → T008+T009 (parallel)
  → T010 → T011 → T012
    → T013 → T014 → T015-T022 (parallel) → T023 → T024 → T025 → T026
      → T027 → T028 → T029-T031
        → T036+T037 (parallel) → T038 → T039 → T040 → T041 → T042
```

---

## Notes

- [P] tasks = different files or independent operations, no dependencies
- [USn] label maps task to specific user story for traceability
- All secrets (DATABASE_URL, BETTER_AUTH_SECRET, GEMINI_API_KEY) must be available at deploy time — stored in `deploy/values.secret.yaml` (gitignored)
- Gordon is the primary tool for Dockerfile work (T010, T011) — fall back to manual editing only if Gordon produces incorrect output
- Kafka topics auto-create on first publish (`auto.create.topics.enable=true` is Bitnami default) — no manual topic creation needed
- Phase I/II/III source code is FROZEN — only new files are added in Phase 4
- Commit after each phase checkpoint; do not batch across phase boundaries
