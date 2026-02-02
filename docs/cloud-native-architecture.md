# Cloud-Native Architecture - AI TaskMaster

## Overview

AI TaskMaster is designed as a cloud-native application following the **12-Factor App** methodology and **Cloud-Native Computing Foundation (CNCF)** best practices. The architecture supports deployment across multiple environments: local development (Docker Compose), staging/production (Kubernetes), and serverless platforms.

---

## Architecture Principles

### 1. Microservices Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Load Balancer                          │
│                  (NGINX Ingress Controller)                   │
└──────────────┬─────────────────────────┬─────────────────────┘
               │                         │
               ▼                         ▼
   ┌─────────────────────┐    ┌─────────────────────┐
   │  Frontend Service   │    │  Backend Service    │
   │   (Next.js App)     │    │   (FastAPI API)     │
   │                     │    │                     │
   │  - React UI         │◄───┤  - REST API         │
   │  - SSR/CSR          │    │  - AI Agents        │
   │  - Authentication   │    │  - Business Logic   │
   └─────────────────────┘    └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Database Service  │
                              │  (PostgreSQL/Neon)  │
                              │                     │
                              │  - Task Storage     │
                              │  - User Data        │
                              │  - Conversations    │
                              └─────────────────────┘
```

### 2. Stateless Services

**Backend (FastAPI)**:
- No server-side sessions
- JWT-based authentication
- All state in database or client
- Horizontally scalable

**Frontend (Next.js)**:
- Cookie-based auth tokens
- Client-side state management
- Static asset caching
- CDN-friendly

### 3. Container-First Design

All services run in containers:
- **Immutable infrastructure**: Containers are never modified, only replaced
- **Portable**: Same container runs in dev, staging, production
- **Reproducible**: `docker build` produces identical image every time

### 4. Declarative Configuration

All infrastructure defined as code:
- Kubernetes manifests (YAML)
- Docker Compose (YAML)
- Environment-based configuration (12-factor)

---

## Deployment Architectures

### Local Development (Docker Compose)

**Purpose**: Developer workstations, fast iteration

```yaml
# Single-command startup
docker-compose up

# Services:
# - postgres: Local PostgreSQL
# - backend: FastAPI with hot-reload
# - frontend: Next.js with hot-reload
# - nginx: Optional reverse proxy
```

**Characteristics**:
- ✅ Fast startup (<30 seconds)
- ✅ Hot module replacement
- ✅ Consistent across developer machines
- ✅ No cloud resources needed

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Staging/Production (Kubernetes)

**Purpose**: Production workloads, scalability, high availability

```
Kubernetes Cluster (3+ nodes)
│
├── Namespace: ai-taskmaster
│   │
│   ├── Deployment: backend (3 replicas)
│   │   ├── Pod 1: backend-6d4b8c7f9d-abc12
│   │   ├── Pod 2: backend-6d4b8c7f9d-def34
│   │   └── Pod 3: backend-6d4b8c7f9d-ghi56
│   │
│   ├── Deployment: frontend (2 replicas)
│   │   ├── Pod 1: frontend-7c9d5e8a2b-jkl78
│   │   └── Pod 2: frontend-7c9d5e8a2b-mno90
│   │
│   ├── Service: backend-service (ClusterIP)
│   ├── Service: frontend-service (ClusterIP)
│   │
│   ├── Ingress: ai-taskmaster-ingress
│   │   ├── Rule: ai-taskmaster.example.com → frontend-service
│   │   └── Rule: api.ai-taskmaster.example.com → backend-service
│   │
│   └── Secrets:
│       ├── postgres-secret (DATABASE_URL)
│       └── app-secrets (GEMINI_API_KEY, BETTER_AUTH_SECRET)
│
└── External: Neon Serverless PostgreSQL
```

**Characteristics**:
- ✅ High availability (3 backend replicas)
- ✅ Auto-scaling (HPA: 2-10 replicas)
- ✅ Zero-downtime deployments (rolling updates)
- ✅ Self-healing (auto-restart unhealthy pods)
- ✅ Load balancing (across replicas)
- ✅ SSL/TLS termination (Ingress)

**Access**:
- Frontend: https://ai-taskmaster.example.com
- Backend API: https://api.ai-taskmaster.example.com

---

## Cloud-Native Patterns

### 1. Health Checks

Every service implements health endpoints:

**Backend `/health`:**
```python
@app.get("/health")
def health_check():
    try:
        # Check database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, detail="unhealthy")
```

**Kubernetes Probes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

### 2. Graceful Shutdown

Services handle SIGTERM for zero-downtime updates:

```python
import signal
import sys

def graceful_shutdown(signum, frame):
    logger.info("Received SIGTERM, shutting down gracefully...")
    # Finish current requests
    # Close database connections
    # Exit cleanly
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
```

**Kubernetes Configuration:**
```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 10"]
terminationGracePeriodSeconds: 30
```

### 3. Resource Management

CPU and memory limits prevent resource starvation:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

**Autoscaling (HPA):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 4. Configuration Management

**Environment Variables (12-Factor):**
```bash
# Development
DATABASE_URL=postgresql://localhost/taskmaster
ENVIRONMENT=development

# Production
DATABASE_URL=postgresql://user:pass@neon.tech/taskmaster?sslmode=require
ENVIRONMENT=production
```

**Kubernetes Secrets:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  GEMINI_API_KEY: <base64-encoded>
  BETTER_AUTH_SECRET: <base64-encoded>
```

### 5. Logging & Observability

**Structured Logging:**
```python
import logging
import json

logger = logging.getLogger("ai-taskmaster")

logger.info("Task created", extra={
    "user_id": user_id,
    "task_id": task_id,
    "correlation_id": correlation_id,
    "timestamp": datetime.utcnow().isoformat()
})
```

**Log Aggregation (ELK Stack):**
```
Pod Logs → Filebeat → Elasticsearch → Kibana
```

**Metrics (Prometheus):**
```
Pod Metrics → Prometheus → Grafana Dashboards
```

**Distributed Tracing:**
- Correlation IDs across all services
- Request tracing through agent pipeline
- Performance profiling

---

## Deployment Workflows

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest backend/tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: |
          docker build -t registry.example.com/backend:${{ github.sha }} ./backend
          docker build -t registry.example.com/frontend:${{ github.sha }} ./frontend
      - name: Push to registry
        run: |
          docker push registry.example.com/backend:${{ github.sha }}
          docker push registry.example.com/frontend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/backend \
            backend=registry.example.com/backend:${{ github.sha }}
          kubectl rollout status deployment/backend
```

### Blue-Green Deployment

```bash
# Deploy green environment
kubectl apply -f kubernetes/backend-green.yaml

# Switch traffic to green
kubectl patch service backend-service -p \
  '{"spec":{"selector":{"version":"green"}}}'

# Verify green is healthy
kubectl logs deployment/backend-green --tail=100

# Delete blue environment
kubectl delete deployment backend-blue
```

### Canary Deployment

```bash
# Deploy canary (10% traffic)
kubectl apply -f kubernetes/backend-canary.yaml
kubectl scale deployment backend-canary --replicas=1

# Monitor metrics
watch kubectl top pods -n ai-taskmaster

# Promote if successful
kubectl scale deployment backend-canary --replicas=3
kubectl scale deployment backend --replicas=0
kubectl delete deployment backend
```

---

## Database Strategy

### Neon Serverless PostgreSQL

**Why Neon:**
- ✅ Serverless (no server management)
- ✅ Auto-scaling (scales with load)
- ✅ Branching (dev/staging/prod databases)
- ✅ Connection pooling (built-in)
- ✅ Free tier (generous limits)

**Connection Pooling:**
```python
from sqlmodel import create_engine

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,           # Max connections
    max_overflow=10,        # Additional connections if needed
    pool_recycle=3600,      # Recycle connections every hour
    pool_pre_ping=True      # Test connection before use
)
```

### Migration Strategy

**Alembic for schema migrations:**
```bash
# Create migration
alembic revision --autogenerate -m "Add conversation tables"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Kubernetes Job for migrations:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: ai-taskmaster-backend:latest
        command: ["alembic", "upgrade", "head"]
      restartPolicy: Never
```

---

## Security Best Practices

### 1. Secrets Management

**Never commit secrets to Git:**
```bash
# .gitignore
.env
.env.local
*.secret
kubernetes/secrets.yaml
```

**Use Kubernetes Secrets:**
```bash
kubectl create secret generic app-secrets \
  --from-literal=GEMINI_API_KEY='...' \
  --from-literal=BETTER_AUTH_SECRET='...' \
  --namespace=ai-taskmaster
```

### 2. Network Policies

Restrict pod-to-pod communication:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
```

### 3. Image Security

**Scan images for vulnerabilities:**
```bash
docker scan ai-taskmaster-backend:latest
```

**Use minimal base images:**
```dockerfile
FROM python:3.13-slim  # Not python:3.13 (full)
```

### 4. RBAC (Role-Based Access Control)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: ai-taskmaster
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
```

---

## Monitoring & Alerting

### Key Metrics

**Application Metrics:**
- Request rate (requests/minute)
- Error rate (4xx, 5xx %)
- Response time (p50, p95, p99)
- Chat endpoint latency (<5s SLA)

**Infrastructure Metrics:**
- CPU usage (per pod)
- Memory usage (per pod)
- Network I/O
- Disk usage

**Database Metrics:**
- Connection pool usage
- Query latency
- Active connections

### Alerts

**Critical Alerts (PagerDuty):**
- Error rate > 10%
- Response time p95 > 10s
- Pod crash loop
- Database connection failure

**Warning Alerts (Slack):**
- Error rate > 5%
- CPU usage > 80%
- Memory usage > 90%

---

## Disaster Recovery

### Backup Strategy

**Database Backups:**
- Automatic daily backups (Neon built-in)
- Point-in-time recovery (30 days)
- Manual backups before major deployments

**Configuration Backups:**
```bash
# Backup Kubernetes manifests
kubectl get all -n ai-taskmaster -o yaml > backup-$(date +%Y%m%d).yaml
```

### Recovery Procedures

**Database Recovery:**
```bash
# Restore from backup
neon restore --backup-id <backup-id> --target-database taskmaster-prod
```

**Deployment Rollback:**
```bash
# Rollback to previous version
kubectl rollout undo deployment/backend -n ai-taskmaster
kubectl rollout undo deployment/frontend -n ai-taskmaster
```

---

## Cost Optimization

### Resource Optimization

**Right-Sizing:**
- Start with minimal resources
- Monitor actual usage
- Adjust based on metrics

**Autoscaling:**
- Scale down during low traffic
- Scale up during peak hours
- Use HPA for automatic adjustments

### Infrastructure Costs

**Development:**
- Docker Compose: Free (local)

**Staging:**
- Neon PostgreSQL: Free tier
- Small Kubernetes cluster: $20-50/month

**Production:**
- Neon PostgreSQL: ~$20/month
- Kubernetes cluster (3 nodes): ~$100-200/month
- Load balancer: ~$20/month
- SSL certificates: Free (Let's Encrypt)
- **Total: ~$140-240/month**

---

## Related Documentation

- [Kubernetes Manifests](../kubernetes/) - K8s YAML files
- [Docker Compose](../docker-compose.yml) - Local development
- [Deploy Skill](../.claude-skills/deploy.md) - Deployment automation
- [K8s Deploy Skill](../.claude-skills/k8s-deploy.md) - Kubernetes helper

---

## Conclusion

AI TaskMaster's cloud-native architecture provides:

✅ **Scalability**: Horizontal scaling from 2 to 10+ replicas
✅ **High Availability**: Multi-replica deployments, auto-restart
✅ **Portability**: Runs on any Kubernetes cluster (GKE, EKS, AKS, Minikube)
✅ **Maintainability**: Declarative configuration, GitOps workflows
✅ **Observability**: Comprehensive logging, metrics, tracing
✅ **Security**: Secrets management, RBAC, network policies
✅ **Cost-Effective**: Auto-scaling, resource optimization

The architecture follows industry best practices and is production-ready for deployment to any cloud provider.
