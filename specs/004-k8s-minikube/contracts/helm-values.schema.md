# Helm Values Contract: `todo-app`

**Purpose**: Defines all configurable parameters for the `todo-app` Helm chart. Every value listed here MUST be present in `charts/todo-app/values.yaml`. Values marked `SECRET` must never have default values — they must be supplied at install time.

---

## Top-Level Structure

```yaml
# charts/todo-app/values.yaml

backend:
  image:
    repository: todo-backend        # local image name (built via docker build)
    tag: latest
    pullPolicy: IfNotPresent
  port: 8000
  replicas: 1                       # 1 for Minikube (resource constrained)
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  healthProbe:
    path: /api/health               # FIXED from legacy /health
    initialDelay: 15
    period: 10
  env:
    CORS_ORIGINS: "http://localhost:3000"
    ENVIRONMENT: "development"

frontend:
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  port: 3000
  replicas: 1
  resources:
    requests:
      memory: "128Mi"
      cpu: "125m"
    limits:
      memory: "256Mi"
      cpu: "250m"
  healthProbe:
    path: /
    initialDelay: 15
    period: 10
  env:
    NEXT_PUBLIC_API_URL: "http://backend-service:8000"

ingress:
  enabled: true
  host: "localhost"                 # Minikube default; override for cloud
  tls:
    enabled: false                  # false for Minikube; true for Phase 5
    secretName: ""

secrets:                            # All SECRET — no defaults allowed
  databaseUrl: ""                   # SECRET: Neon PostgreSQL connection string
  betterAuthSecret: ""              # SECRET: JWT signing secret (32+ chars)
  geminiApiKey: ""                  # SECRET: Google Gemini API key

dapr:
  enabled: true
  appId:
    backend: "todo-backend"
    frontend: "todo-frontend"
  pubsub:
    name: "todo-pubsub"
    broker: "kafka.ai-taskmaster.svc.cluster.local:9092"
  statestore:
    name: "todo-statestore"
    redis: "redis.ai-taskmaster.svc.cluster.local:6379"

kafka:
  enabled: true                     # deploys Bitnami Kafka sub-chart
  topics:                           # auto-created on first publish
    - todo.tasks.created
    - todo.tasks.updated
    - todo.tasks.completed
    - todo.tasks.deleted

redis:
  enabled: true                     # deploys Bitnami Redis sub-chart

kagent:
  enabled: true                     # install kagent in separate namespace
  namespace: kagent
```

---

## Install-Time Secrets Example

Secrets are supplied via `--set` or a values override file (not committed to source control):

```bash
helm install todo-app ./charts/todo-app \
  --set secrets.databaseUrl="postgresql+psycopg://..." \
  --set secrets.betterAuthSecret="<32-char-secret>" \
  --set secrets.geminiApiKey="<gemini-key>"
```

Or via a `.env`-derived values file (gitignored):

```bash
# deploy/values.secret.yaml  (in .gitignore)
secrets:
  databaseUrl: "postgresql+psycopg://..."
  betterAuthSecret: "..."
  geminiApiKey: "..."

helm install todo-app ./charts/todo-app -f deploy/values.secret.yaml
```
