# Quickstart: Phase 4 — Deploy Todo App on Minikube

**Branch**: `004-k8s-minikube` | **Date**: 2026-02-03
**Audience**: Developer with Docker Desktop already running on Windows.
**Estimated time**: ~30 minutes (first run, including tool installation).

---

## Prerequisites (already confirmed)

| Tool | Status | Version |
|------|--------|---------|
| Docker Desktop | Installed | 4.55.0 |
| Gordon (Docker AI) | Enabled | Built into Docker Desktop |
| kubectl | Installed | v1.34.1 |

---

## Step 0: Enable Gordon

1. Open Docker Desktop → **Settings** → **Beta features**
2. Toggle **Docker AI** on
3. Verify: run `docker ai "What can you do?"` in PowerShell

---

## Step 1: Install Missing Tools

Run all commands in **PowerShell as Administrator** unless noted.

### 1a. Minikube

```powershell
# Download and run the installer
Invoke-WebRequest -Uri "https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe" -OutFile minikube-installer.exe
Start-Process .\minikube-installer.exe -Wait
# Verify
minikube version
```

### 1b. Helm

```powershell
# Download latest Helm release (check https://github.com/helm/helm/releases for latest tag)
Invoke-WebRequest -Uri "https://get.helm.sh/helm-v3.16.0-windows-amd64.zip" -OutFile helm.zip
Expand-Archive -Path helm.zip -DestinationPath .\helm-extract
Copy-Item .\helm-extract\windows-amd64\helm.exe -Destination "C:\Program Files\Kubernetes\"
# Add C:\Program Files\Kubernetes\ to PATH if not already there
helm version
```

### 1c. kubectl-ai (Google)

```powershell
Invoke-WebRequest -Uri "https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Windows_x86_64.zip" -OutFile kubectl-ai.zip
Expand-Archive -Path kubectl-ai.zip -DestinationPath "C:\kubectl-ai" -Force
# Add C:\kubectl-ai to PATH via System > Environment Variables
# Set your Gemini API key:
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-key-here", "Machine")
# Verify (new terminal session required)
kubectl-ai --help
```

### 1d. Dapr CLI

```powershell
Invoke-WebRequest -Uri "https://github.com/dapr/cli/releases/latest/download/dapr_windows_amd64.zip" -OutFile dapr.zip
Expand-Archive -Path dapr.zip -DestinationPath "C:\dapr-cli" -Force
# Add C:\dapr-cli to PATH
dapr version
```

---

## Step 2: Start Minikube

```powershell
# Use Docker Desktop as the driver (reuses existing Docker engine)
minikube start --driver=docker --memory=4096 --cpus=2

# Enable required addons
minikube addons enable ingress
minikube addons enable dashboard
minikube addons enable metrics-server

# Verify
kubectl get nodes
# Expected: one node in "Ready" state
```

---

## Step 3: Install Dapr on the Cluster

```powershell
dapr init -k
# Wait for "Dapr has been installed to your Kubernetes cluster" message

# Verify
kubectl get pods -n dapr-system
# Expected: dapr-operator, dapr-injector, dapr-placement-server, dapr-sidecar-injector — all Running
```

---

## Step 4: Build Container Images

Use Gordon for AI-assisted Dockerfile creation/debugging:

```powershell
# Backend (Dockerfile exists — Gordon can review/fix it)
docker ai "Review backend/Dockerfile and fix any issues"
cd backend
docker build -t todo-backend .

# Frontend (Dockerfile needs to be created — use Gordon)
docker ai "Create a production Dockerfile for a Next.js app in the frontend/ directory"
cd ..\frontend
docker build -t todo-frontend .

# Verify both images
docker images | grep todo-
```

---

## Step 5: Deploy with Helm

```powershell
cd <repo-root>

# Create the secrets values file (gitignored — never commit)
# Edit deploy/values.secret.yaml with your actual secrets:
#   secrets.databaseUrl  = your Neon PostgreSQL URL
#   secrets.betterAuthSecret = your 32-char secret
#   secrets.geminiApiKey = your Gemini API key

# Deploy
helm install todo-app ./charts/todo-app -f deploy/values.secret.yaml

# Wait for pods
kubectl get pods -n ai-taskmaster -w
# Wait until backend and frontend pods show Running/Ready
```

---

## Step 6: Install Kagent

```powershell
# Install CRDs
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds --namespace kagent --create-namespace

# Install Kagent (uses your API key)
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent --namespace kagent `
  --set providers.openAI.apiKey=$env:OPENAI_API_KEY

# Open Kagent dashboard
kagent dashboard
```

---

## Step 7: Access the Application

```powershell
# Start the Minikube ingress tunnel (keep this running in a terminal)
minikube tunnel

# Open in browser:
# http://localhost/       → Frontend (login page)
# http://localhost/api/health → Backend health check (should return {"status":"healthy"})
```

---

## Step 8: Verify Events (Kafka)

```powershell
# Use kubectl-ai to check Kafka
kubectl-ai "show me the pods in the ai-taskmaster namespace"

# Or manually consume from a Kafka topic:
kubectl exec -it <kafka-pod> -n ai-taskmaster -- kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic todo.tasks.created --from-beginning
```

---

## Step 9: AI-Assisted Operations

```powershell
# kubectl-ai examples
kubectl-ai "check why the backend pods are failing"
kubectl-ai "scale the backend to 2 replicas"
kubectl-ai "show resource usage across all pods"

# Kagent examples (via dashboard or CLI)
kagent invoke -t "analyze the cluster health" --agent k8s-agent
kagent invoke -t "What Helm charts are installed?" --agent helm-agent
```

---

## Teardown

```powershell
helm uninstall todo-app
helm uninstall kagent -n kagent
helm uninstall kagent-crds -n kagent
dapr uninstall -k
minikube stop   # or minikube delete to remove entirely
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Pod stuck in `Pending` | Minikube out of memory | `minikube stop && minikube start --memory=6144` |
| Backend `CrashLoopBackOff` | Missing secret env var | Check `kubectl logs <pod> -n ai-taskmaster`; verify secrets |
| Ingress returns 404 | Tunnel not running | Run `minikube tunnel` in a separate terminal |
| Dapr sidecar not injected | Namespace missing label | `kubectl label namespace ai-taskmaster dapr.io/enabled=true` |
| Kafka topic empty | Events not published | Check backend logs for pub/sub errors; verify Dapr component |
