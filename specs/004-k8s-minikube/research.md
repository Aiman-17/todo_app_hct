# Research: Phase 4 — Local Kubernetes Deployment

**Branch**: `004-k8s-minikube` | **Date**: 2026-02-03
**Purpose**: Resolve all unknowns from Technical Context before design phase.

---

## Decision 1: Docker AI Agent (Gordon)

**Decision**: Use Gordon for initial Dockerfile generation and container troubleshooting.

**Rationale**: Docker Desktop 4.55.0 is already installed and Gordon responded successfully to `docker ai "What can you do?"`. It is the hackathon-mandated tool for Docker operations. Gordon generates Dockerfiles interactively and can debug container issues in-place — faster than manual iteration.

**Alternatives considered**:
- Standard `docker build` CLI only — still the fallback if Gordon produces incorrect output, but Gordon is the primary tool per requirements.

**Current state gap**: `backend/Dockerfile` exists but has a port mismatch (exposes 7860 instead of 8000). `frontend/Dockerfile` does not exist. Both need to be created/fixed — Gordon is the tool to use for this.

---

## Decision 2: Minikube as the Local Cluster

**Decision**: Use Minikube with the Docker Desktop driver (already available).

**Rationale**: Docker Desktop's kubectl (v1.34.1) is already installed. Minikube with `--driver=docker` reuses Docker Desktop's engine and avoids needing a separate VM hypervisor. This is the lightest-weight option on the developer's Windows machine.

**Installation**: Via the official `minikube-installer.exe` from [minikube releases](https://kubernetes.io/docs/tasks/tools/install-minikube/). After install, start with `minikube start --driver=docker`.

**Alternatives considered**:
- Kind (Kubernetes in Docker) — similar capability but less tooling ecosystem for Dapr.
- Docker Desktop's built-in Kubernetes — limited; does not support Dapr sidecar injection cleanly.

---

## Decision 3: Helm for Package Management

**Decision**: Use Helm v3 to package the entire application stack as a single chart with sub-charts for dependencies (Kafka, Redis, Dapr components).

**Rationale**: Helm is the de-facto Kubernetes package manager. It enables single-command deploy/teardown (matching SC-001, SC-005). The existing raw manifests in `kubernetes/` will be migrated into the Helm chart structure.

**Installation**: Download `helm.exe` from [Helm releases](https://github.com/helm/helm/releases) and place in PATH.

**Alternatives considered**:
- Raw `kubectl apply` with the existing `kubernetes/` manifests — works but does not support parameterised deployments, dependency management, or clean teardown of the full stack.

---

## Decision 4: kubectl-ai (Google) for AI-Assisted K8s Operations

**Decision**: Use [GoogleCloudPlatform/kubectl-ai](https://github.com/GoogleCloudPlatform/kubectl-ai) — the actively maintained Google project.

**Rationale**: Two projects share the name `kubectl-ai`. The Google version is actively maintained, supports multiple LLM backends (including Gemini, which the project already has a key for via `GEMINI_API_KEY`), and works as an interactive shell. It does not deploy workloads directly — it generates and explains kubectl commands via natural language.

**Installation** (PowerShell, admin):
```powershell
Invoke-WebRequest -Uri "https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Windows_x86_64.zip" -OutFile kubectl-ai.zip
Expand-Archive -Path kubectl-ai.zip -DestinationPath "C:\kubectl-ai" -Force
# Add C:\kubectl-ai to PATH via System Environment Variables
```
Set `GEMINI_API_KEY` environment variable before first use.

**Alternatives considered**:
- sozercan/kubectl-ai (older, Krew-based) — less maintained; Google version is preferred.

---

## Decision 5: Kagent for Cluster-Level AI Operations

**Decision**: Install Kagent via Helm into the Minikube cluster. Use it for cluster health analysis and resource optimization.

**Rationale**: Kagent is a Kubernetes-native AI agent framework (CNCF sandbox project by Solo.io). It runs inside the cluster, making it context-aware. It ships as Helm charts and supports OpenAI/Gemini/Anthropic backends. The hackathon requirements list it as a required tool.

**Installation** (after Minikube and Helm are ready):
```bash
# Install CRDs first
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds --namespace kagent --create-namespace

# Install main chart (use GEMINI_API_KEY or OPENAI_API_KEY)
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent --namespace kagent \
  --set providers.openAI.apiKey=$OPENAI_API_KEY
```

**Alternatives considered**:
- Manual kubectl + shell scripts for cluster monitoring — works but does not satisfy the hackathon requirement for AI-assisted K8s ops.

---

## Decision 6: Dapr on Kubernetes (CLI + Helm)

**Decision**: Install Dapr runtime on Minikube using the Dapr CLI (`dapr init -k`). Deploy Dapr components (pub/sub Kafka, state store Redis) as Kubernetes custom resources.

**Rationale**: Dapr CLI is the simplest path to sidecar injection on Minikube. The `-k` flag targets the current kube context. Dapr auto-injects sidecars when pods carry the `dapr.io/enabled: "true"` annotation.

**Installation**: Download `dapr` CLI from [Dapr releases](https://github.com/dapr/cli/releases) (Windows x64 zip), place in PATH, then run `dapr init -k`.

**Alternatives considered**:
- Helm-only Dapr install — more flexible for production but the CLI path is faster for local dev and is the documented Minikube flow in [Dapr docs](https://docs.dapr.io/operations/hosting/kubernetes/cluster/setup-minikube/).

---

## Decision 7: Kafka Deployment Strategy

**Decision**: Deploy Kafka inside Minikube using the [Bitnami Kafka Helm chart](https://charts.bitnami.com/bitnami). Wire it as a Dapr pub/sub component.

**Rationale**: Bitnami charts are battle-tested, widely used, and support single-node mode (appropriate for local dev resource constraints). The Dapr pub/sub component YAML simply points to the in-cluster Kafka service.

**Kafka topic naming**: `todo.tasks.created`, `todo.tasks.updated`, `todo.tasks.completed`, `todo.tasks.deleted` — per constitution Principle VI.

**Alternatives considered**:
- External managed Kafka — unnecessary for local dev; adds network dependency.
- Dapr's built-in sample broker — limited; Bitnami gives a real Kafka instance for realistic testing.

---

## Decision 8: Redis for Dapr State Store

**Decision**: Deploy Redis inside Minikube using the Bitnami Redis Helm chart. Wire as a Dapr state store component.

**Rationale**: Redis is Dapr's default and recommended state store backing. Bitnami chart is minimal and fast to deploy. Matches the spec assumption.

**Alternatives considered**:
- In-memory state store — does not survive pod restarts; violates User Story 4 acceptance scenario 2.

---

## Decision 9: Ingress Controller

**Decision**: Use Minikube's built-in nginx ingress addon (`minikube addons enable ingress`). Strip TLS/cert-manager annotations from the existing ingress manifest for local dev.

**Rationale**: The existing `kubernetes/ingress.yaml` targets production (cert-manager, TLS). Minikube's built-in nginx addon serves HTTP on `localhost` with no TLS setup required. TLS will be re-enabled in Phase 5 (cloud).

**Alternatives considered**:
- Traefik — supported but Minikube's default addon is nginx; less configuration.

---

## Existing Artifact Issues (to fix in Phase 4)

| File | Issue | Fix |
|------|-------|-----|
| `backend/Dockerfile` | Exposes port 7860 (HuggingFace legacy); K8s manifests expect 8000 | Change EXPOSE and CMD port to 8000 |
| `backend/Dockerfile` | Uses Python 3.12; `requirements.txt` targets 3.13+ | Update base image to `python:3.13-slim` |
| `kubernetes/backend-deployment.yaml` | Health probe path is `/health`; actual endpoint is `/api/health` | Fix in Helm chart templates |
| `kubernetes/ingress.yaml` | Production TLS annotations (cert-manager) | Strip for Minikube; parameterise via Helm values |
| `frontend/Dockerfile` | Does not exist | Create via Gordon |

---

## Sources

- [kubectl-ai GitHub (Google)](https://github.com/GoogleCloudPlatform/kubectl-ai)
- [kagent quickstart](https://kagent.dev/docs/kagent/getting-started/quickstart)
- [Dapr — Setup Minikube](https://docs.dapr.io/operations/hosting/kubernetes/cluster/setup-minikube/)
- [Dapr — Deploy on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/)
- [Minikube install on Windows](https://john-cd.com/cheatsheets/Containers/Minikube_Install_on_Windows/)
- [Minikube + Dapr + Helm WSL2 setup](https://github.com/tobycouchmanmicrosoft/Minikubek8sWsl2Setup)
