# Feature Specification: Local Kubernetes Deployment (Minikube)

**Feature Branch**: `004-k8s-minikube`
**Created**: 2026-02-03
**Status**: Draft
**Input**: Phase 4 — Containerize backend and frontend, deploy to Minikube via Helm, integrate Dapr sidecars for Kafka pub/sub and state store, wire service mesh via Dapr service invocation.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Containerize and Run Services Locally (Priority: P1)

A developer checks out the project and builds container images for both the backend and frontend services. They run both containers locally and confirm that the application behaves identically to the Vercel-hosted version — login, task CRUD, and AI chatbot all work.

**Why this priority**: Containerization is the prerequisite for everything else in Phase 4. Without working images, Helm deployment and Dapr integration cannot proceed. This story alone delivers verifiable value: a fully portable, runnable application.

**Independent Test**: Build both images, start them with a local container orchestrator, hit the frontend in a browser, create a task via the chatbot, and confirm it persists.

**Acceptance Scenarios**:

1. **Given** the project source code, **When** a developer runs the container build for the backend, **Then** a valid image is produced with no build errors.
2. **Given** the project source code, **When** a developer runs the container build for the frontend, **Then** a valid image is produced with no build errors.
3. **Given** both images built, **When** both containers are started with correct environment variables, **Then** the frontend is reachable and all Phase III features function correctly.

---

### User Story 2 — Deploy Full Stack to Minikube via Helm (Priority: P2)

A developer runs a single Helm install command against their local Minikube cluster. All application services (backend, frontend, ingress) come up as Kubernetes pods. The developer accesses the app through the Minikube ingress URL and uses it end-to-end.

**Why this priority**: Helm-based deployment is the core deliverable of Phase 4. It proves the application is Kubernetes-native and sets the foundation for cloud deployment in Phase 5.

**Independent Test**: Run Helm install, wait for all pods to reach Ready state, open the ingress URL in a browser, log in, and perform a complete task workflow.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** a developer runs the Helm install command, **Then** all required pods (backend, frontend) reach Ready state within 2 minutes.
2. **Given** all pods are Ready, **When** a developer opens the Minikube ingress URL, **Then** the login page loads and the full application is usable.
3. **Given** the app is running on Minikube, **When** a developer performs task CRUD and chatbot operations, **Then** all data persists correctly (no regression from Phase III behavior).

---

### User Story 3 — Event-Driven Task Operations via Dapr and Kafka (Priority: P3)

When a developer creates, updates, completes, or deletes a task through the application (via chatbot or direct UI), the backend publishes a corresponding event to a Kafka topic through the Dapr pub/sub sidecar. A consumer of that topic can observe the event in real time.

**Why this priority**: Event-driven architecture is a constitutional requirement (Principle VI). Phase 4 establishes the pub/sub plumbing; Phase 5 relies on it being production-ready.

**Independent Test**: Deploy the stack, perform a task action, then inspect the Kafka topic for the published event using a CLI consumer tool.

**Acceptance Scenarios**:

1. **Given** the full stack is deployed with Dapr and Kafka, **When** a task is created via the chatbot, **Then** a `todo.tasks.created` event appears on the corresponding Kafka topic.
2. **Given** the full stack is deployed, **When** a task is completed, **Then** a `todo.tasks.completed` event is published.
3. **Given** the Kafka broker is temporarily unavailable, **When** a task operation is performed, **Then** the operation itself succeeds and a warning is logged (event delivery is best-effort in Phase 4).

---

### User Story 4 — Dapr State Store Integration (Priority: P4)

The Dapr sidecar provides a local state store (backed by an in-cluster key-value store) that services can use for caching or session data. The state store is accessible via the standard Dapr state API from within the cluster.

**Why this priority**: State store is part of the Dapr component suite required by the constitution. Phase 4 wires it; Phase 5 may swap the backing store for a cloud-managed equivalent.

**Independent Test**: From a backend pod, issue a Dapr state store get/set call and confirm data round-trips correctly.

**Acceptance Scenarios**:

1. **Given** Dapr sidecars are running, **When** the backend writes a value to the state store, **Then** the value is retrievable via the same Dapr state API.
2. **Given** the state store is configured, **When** the pod restarts, **Then** previously stored values survive (backed by persistent storage).

---

### Edge Cases

- What happens when a backend pod crashes mid-request? Kubernetes restart policy recovers the pod; the in-flight request returns an error to the client. No data corruption occurs because the database transaction either committed or rolled back.
- How does the system handle Kafka broker unavailability? Task operations complete via the synchronous database path. Event publishing fails gracefully; a warning is logged. No user-facing error is surfaced.
- What happens when Minikube runs out of memory or CPU? Pods enter a Pending state with a clear resource-related reason. Existing healthy pods continue serving traffic.
- What happens during a rolling update of the backend? New pods start alongside old ones; ingress routes traffic only to Ready pods. Zero downtime is achieved if at least one replica remains healthy.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The backend service MUST be packaged as a self-contained container image that starts and serves HTTP traffic without any host-level dependencies beyond a container runtime.
- **FR-002**: The frontend service MUST be packaged as a self-contained container image that builds the Next.js application and serves it in production mode.
- **FR-003**: Both container images MUST be buildable using a single, repeatable command from the project root with no manual steps.
- **FR-004**: A Helm chart MUST declare all Kubernetes resources required to run the application: Deployments, Services, ConfigMaps, Secrets, an Ingress, and Dapr Component manifests.
- **FR-005**: The full application stack MUST be deployable to Minikube with a single `helm install` command (plus any prerequisite namespace/addon setup documented in a runbook).
- **FR-006**: Dapr sidecars MUST be automatically injected into backend and frontend pods via the Dapr Kubernetes runtime.
- **FR-007**: A Kafka message broker MUST be deployed within the Minikube cluster as a Dapr pub/sub component.
- **FR-008**: The backend MUST publish task lifecycle events (`created`, `updated`, `completed`, `deleted`) to Kafka topics following the naming convention `todo.<domain>.<event-type>`.
- **FR-009**: A Dapr state store component MUST be deployed and accessible to all sidecars within the cluster.
- **FR-010**: All pods MUST have liveness and readiness probes configured so that Kubernetes can detect and recover unhealthy instances.
- **FR-011**: All secrets (database credentials, API keys) MUST be stored as Kubernetes Secrets; no secret values may appear in source-controlled YAML or code.
- **FR-012**: Services MUST communicate within the cluster using Dapr service invocation (not direct pod-to-pod HTTP calls).
- **FR-013**: The frontend MUST be exposed via a Kubernetes Ingress resource accessible from the Minikube host at a documented local URL.

### Key Entities

- **Container Image**: A portable, self-contained snapshot of a service (backend or frontend) and all its runtime dependencies. Two images are produced: one per service.
- **Helm Chart**: A versioned, declarative package that describes the complete Kubernetes deployment topology — all resources, their relationships, and configurable parameters.
- **Dapr Component**: A configuration artifact that binds a Dapr capability (pub/sub, state store) to a concrete backing technology (Kafka, Redis). Deployed as Kubernetes custom resources.
- **Kafka Topic**: A named, ordered event channel within the broker. Topics follow the `todo.<domain>.<event-type>` naming convention defined in the project constitution.
- **Ingress**: The single external entry point that routes inbound traffic from the host machine into the appropriate Kubernetes service.

### Assumptions

- Minikube is pre-installed and operational on the developer machine. Docker Desktop is confirmed working (Phase 4 prerequisite gate).
- The database remains the external Neon PostgreSQL instance used in Phases II and III. It is NOT replicated inside Minikube. The backend connects to it over the network from within the cluster (identical to the Vercel deployment).
- Service mesh is provided exclusively by Dapr's built-in service invocation. No additional service mesh (Istio, Linkerd) is deployed in Phase 4. This keeps scope focused and avoids duplicating capabilities Dapr already provides.
- Kafka is deployed as a self-hosted broker inside Minikube (e.g., via Bitnami Helm chart or Dapr's built-in sample). No external managed Kafka service is required.
- The Dapr state store backing store is Redis, deployed in-cluster.
- Phase I, II, and III application code is frozen. Phase 4 adds only: Dockerfiles, Helm chart, Dapr component YAMLs, and a deployment runbook. No changes to existing backend or frontend source code.
- Cloud deployment target (DOKS/GKE/AKS) is out of scope for Phase 4 and will be addressed in Phase 5. Helm charts are written to be cloud-provider-agnostic where possible.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The full application stack (backend, frontend, Dapr, Kafka, ingress) deploys to a fresh Minikube cluster from a single Helm install command in under 5 minutes.
- **SC-002**: All pods reach a healthy and Ready state within 2 minutes of the Helm install completing, with zero manual intervention required.
- **SC-003**: Every task lifecycle action (create, update, complete, delete) performed through the application results in a corresponding event being published to the correct Kafka topic.
- **SC-004**: All Phase III functionality — task CRUD via the UI, AI chatbot task management, user authentication — works identically on the Minikube deployment as it does on Vercel. Zero regression.
- **SC-005**: The deployment can be cleanly torn down (`helm uninstall`) and redeployed from scratch with no leftover state or manual cleanup required.
- **SC-006**: No secrets, API keys, or credentials appear in any source-controlled file. All sensitive values are injected at deploy time via Kubernetes Secrets or environment variables.
