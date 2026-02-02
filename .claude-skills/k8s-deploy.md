# K8s Deploy - Kubernetes Deployment Helper Skill

## Description
Interactive Kubernetes deployment helper for AI TaskMaster. Provides guided deployment workflows, troubleshooting assistance, and health monitoring for Kubernetes clusters.

## Usage
```
/k8s-deploy [action] [--namespace NAME] [--environment ENV]
```

**Actions:**
- `init` - Initialize Kubernetes namespace and secrets
- `apply` - Apply all Kubernetes manifests
- `status` - Check deployment status
- `scale` - Scale replicas up/down
- `rollback` - Rollback to previous version
- `logs` - View pod logs
- `shell` - Open shell in pod

**Examples:**
```bash
/k8s-deploy init                           # Setup namespace and secrets
/k8s-deploy apply --environment production # Deploy to production
/k8s-deploy status                         # Check current status
/k8s-deploy scale backend 5                # Scale backend to 5 replicas
/k8s-deploy rollback backend               # Rollback backend deployment
```

## Quick Start

### 1. Initialize Cluster
```bash
# Create namespace
kubectl create namespace ai-taskmaster

# Create secrets
kubectl create secret generic postgres-secret \
  --from-literal=DATABASE_URL='postgresql://user:pass@host/db' \
  --namespace=ai-taskmaster

kubectl create secret generic app-secrets \
  --from-literal=GEMINI_API_KEY='your-gemini-key' \
  --from-literal=BETTER_AUTH_SECRET='your-auth-secret' \
  --namespace=ai-taskmaster

# Verify secrets
kubectl get secrets -n ai-taskmaster
```

### 2. Deploy Application
```bash
# Apply all manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml
kubectl apply -f kubernetes/ingress.yaml

# Or apply all at once
kubectl apply -f kubernetes/ -n ai-taskmaster
```

### 3. Verify Deployment
```bash
# Check pod status
kubectl get pods -n ai-taskmaster

# Expected output:
# NAME                        READY   STATUS    RESTARTS   AGE
# backend-6d4b8c7f9d-abc12    1/1     Running   0          2m
# backend-6d4b8c7f9d-def34    1/1     Running   0          2m
# frontend-7c9d5e8a2b-ghi56   1/1     Running   0          2m
# frontend-7c9d5e8a2b-jkl78   1/1     Running   0          2m
# postgres-0                  1/1     Running   0          5m

# Check services
kubectl get svc -n ai-taskmaster

# Check deployment rollout status
kubectl rollout status deployment/backend -n ai-taskmaster
kubectl rollout status deployment/frontend -n ai-taskmaster
```

## Deployment Workflows

### Production Deployment Workflow

```mermaid
graph TD
    A[Tag & Build Images] --> B[Push to Registry]
    B --> C[Update Manifests]
    C --> D[Create Backup]
    D --> E[Apply Manifests]
    E --> F{Rollout Success?}
    F -->|Yes| G[Run Smoke Tests]
    F -->|No| H[Rollback]
    G --> I{Tests Pass?}
    I -->|Yes| J[Mark Deployed]
    I -->|No| H
    H --> K[Investigate Logs]
```

**Step-by-Step Commands:**

```bash
# 1. Build and tag
export VERSION=v1.2.3
docker build -t ai-taskmaster-backend:$VERSION ./backend
docker build -t ai-taskmaster-frontend:$VERSION ./frontend

# 2. Push to registry
docker tag ai-taskmaster-backend:$VERSION registry.example.com/backend:$VERSION
docker push registry.example.com/backend:$VERSION

# 3. Backup current state
kubectl get deployment backend -n ai-taskmaster -o yaml > backup-backend-$(date +%Y%m%d-%H%M%S).yaml

# 4. Update image in deployment
kubectl set image deployment/backend \
  backend=registry.example.com/backend:$VERSION \
  -n ai-taskmaster

# 5. Monitor rollout
kubectl rollout status deployment/backend -n ai-taskmaster --timeout=5m

# 6. Verify pods running
kubectl get pods -n ai-taskmaster -l app=backend

# 7. Run smoke tests
kubectl exec -n ai-taskmaster deployment/backend -- \
  curl -f http://localhost:8000/health
```

### Canary Deployment

Deploy to small subset of users first:

```bash
# 1. Create canary deployment
kubectl apply -f kubernetes/backend-canary.yaml

# 2. Route 10% traffic to canary
kubectl patch service backend -n ai-taskmaster -p \
  '{"spec":{"selector":{"version":"canary","percentage":"10"}}}'

# 3. Monitor metrics
kubectl logs -n ai-taskmaster deployment/backend-canary --tail=100 -f

# 4. Promote canary if successful
kubectl scale deployment/backend-canary --replicas=3 -n ai-taskmaster
kubectl scale deployment/backend --replicas=0 -n ai-taskmaster
kubectl delete deployment backend -n ai-taskmaster
kubectl rename deployment backend-canary backend

# 5. Or rollback if issues
kubectl delete deployment backend-canary -n ai-taskmaster
```

## Scaling Operations

### Manual Scaling
```bash
# Scale backend to 5 replicas
kubectl scale deployment/backend --replicas=5 -n ai-taskmaster

# Scale frontend to 3 replicas
kubectl scale deployment/frontend --replicas=3 -n ai-taskmaster

# Verify scaling
kubectl get pods -n ai-taskmaster -w  # Watch in real-time
```

### Auto-Scaling (HPA)
```bash
# Create HorizontalPodAutoscaler
kubectl autoscale deployment backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n ai-taskmaster

# Check HPA status
kubectl get hpa -n ai-taskmaster

# Expected output:
# NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
# backend   Deployment/backend   45%/70%   2         10        3          5m
```

### Resource Management
```bash
# View resource usage
kubectl top pods -n ai-taskmaster

# View resource requests/limits
kubectl describe deployment backend -n ai-taskmaster | grep -A 5 "Limits:"

# Update resources
kubectl set resources deployment backend \
  --limits=cpu=1,memory=1Gi \
  --requests=cpu=500m,memory=512Mi \
  -n ai-taskmaster
```

## Troubleshooting Guide

### Pod Not Starting

**Symptom:** Pod stuck in `Pending`, `CrashLoopBackOff`, or `ImagePullBackOff`

```bash
# Check pod status
kubectl get pods -n ai-taskmaster

# Describe pod for events
kubectl describe pod <pod-name> -n ai-taskmaster

# Common issues and solutions:
```

**ImagePullBackOff:**
```bash
# Check image name
kubectl get pod <pod-name> -n ai-taskmaster -o jsonpath='{.spec.containers[0].image}'

# Check image pull secret
kubectl get secret -n ai-taskmaster

# Fix: Update deployment with correct image
kubectl set image deployment/backend backend=correct-image:tag -n ai-taskmaster
```

**CrashLoopBackOff:**
```bash
# Check logs
kubectl logs <pod-name> -n ai-taskmaster --previous

# Common causes:
# - Missing environment variables
# - Database connection failure
# - Application error on startup

# Fix: Check environment variables
kubectl get deployment backend -n ai-taskmaster -o yaml | grep -A 10 env:
```

**Pending (Insufficient Resources):**
```bash
# Check node capacity
kubectl describe nodes | grep -A 5 "Allocated resources"

# Fix: Scale down other deployments or add nodes
kubectl scale deployment other-app --replicas=1
```

### Database Connection Issues

```bash
# Test database connectivity from pod
kubectl exec -n ai-taskmaster deployment/backend -- \
  python -c "from sqlmodel import create_engine; import os; engine = create_engine(os.getenv('DATABASE_URL')); engine.connect()"

# Check database secret
kubectl get secret postgres-secret -n ai-taskmaster -o yaml

# Verify DATABASE_URL format
kubectl exec -n ai-taskmaster deployment/backend -- \
  printenv DATABASE_URL
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints backend -n ai-taskmaster

# If no endpoints:
# - Check pod selector matches deployment labels
kubectl get svc backend -n ai-taskmaster -o yaml | grep selector -A 2
kubectl get pods -n ai-taskmaster -l app=backend --show-labels

# Test service from within cluster
kubectl run curl-test --image=curlimages/curl -it --rm -n ai-taskmaster -- \
  curl http://backend-service:8000/health

# Check ingress
kubectl get ingress -n ai-taskmaster
kubectl describe ingress -n ai-taskmaster
```

## Health Monitoring

### Liveness & Readiness Probes

```yaml
# Liveness probe (restart if failing)
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# Readiness probe (remove from service if failing)
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

### Check Probe Status
```bash
# View probe failures
kubectl describe pod <pod-name> -n ai-taskmaster | grep -A 10 "Events:"

# Manual health check
kubectl exec -n ai-taskmaster deployment/backend -- \
  curl -f http://localhost:8000/health
```

## Log Management

### View Logs
```bash
# Tail logs from all backend pods
kubectl logs -n ai-taskmaster deployment/backend --tail=100 -f

# Logs from specific pod
kubectl logs <pod-name> -n ai-taskmaster

# Logs from previous container (if crashed)
kubectl logs <pod-name> -n ai-taskmaster --previous

# Logs with timestamps
kubectl logs <pod-name> -n ai-taskmaster --timestamps
```

### Log Aggregation
```bash
# Stream logs from all pods with label
kubectl logs -n ai-taskmaster -l app=backend --all-containers=true -f

# Save logs to file
kubectl logs deployment/backend -n ai-taskmaster > backend-logs.txt

# Filter logs
kubectl logs deployment/backend -n ai-taskmaster | grep ERROR
```

## Database Operations

### Run Migrations
```bash
# Run Alembic migrations
kubectl exec -n ai-taskmaster deployment/backend -- \
  alembic upgrade head

# Check migration status
kubectl exec -n ai-taskmaster deployment/backend -- \
  alembic current

# Rollback migration
kubectl exec -n ai-taskmaster deployment/backend -- \
  alembic downgrade -1
```

### Database Backup
```bash
# Backup database from pod
kubectl exec -n ai-taskmaster postgres-0 -- \
  pg_dump -U postgres taskmaster > backup-$(date +%Y%m%d).sql

# Restore from backup
kubectl exec -i -n ai-taskmaster postgres-0 -- \
  psql -U postgres taskmaster < backup-20260130.sql
```

## Useful Commands Cheat Sheet

```bash
# Quick status check
kubectl get all -n ai-taskmaster

# Port forwarding for local testing
kubectl port-forward -n ai-taskmaster deployment/backend 8000:8000
kubectl port-forward -n ai-taskmaster deployment/frontend 3000:3000

# Execute command in pod
kubectl exec -it -n ai-taskmaster deployment/backend -- /bin/bash

# Copy files to/from pod
kubectl cp file.txt ai-taskmaster/backend-pod:/tmp/file.txt
kubectl cp ai-taskmaster/backend-pod:/app/logs.txt ./logs.txt

# Delete and recreate deployment (clean slate)
kubectl delete deployment backend -n ai-taskmaster
kubectl apply -f kubernetes/backend-deployment.yaml

# Restart deployment (rolling restart)
kubectl rollout restart deployment/backend -n ai-taskmaster

# View resource quotas
kubectl describe resourcequota -n ai-taskmaster

# View events
kubectl get events -n ai-taskmaster --sort-by='.lastTimestamp'
```

## Best Practices

✅ **Always use namespaces** for isolation
✅ **Set resource limits and requests** to prevent resource starvation
✅ **Use liveness and readiness probes** for health checks
✅ **Enable autoscaling (HPA)** for production workloads
✅ **Use ConfigMaps** for configuration, Secrets for sensitive data
✅ **Tag images with versions**, never use `:latest` in production
✅ **Implement graceful shutdown** (handle SIGTERM)
✅ **Use rolling updates** for zero-downtime deployments
✅ **Monitor pod metrics** (CPU, memory, network)
✅ **Set up log aggregation** (ELK, Loki) for production

## Related Documentation

- [Kubernetes Manifests](../kubernetes/) - K8s YAML files
- [Deploy Skill](./deploy.md) - Full deployment automation
- [Cloud-Native Architecture](../docs/cloud-native-architecture.md)

## Skill Metadata

- **Type**: DevOps Helper
- **Category**: Kubernetes, Deployment
- **Complexity**: Medium-High
- **Requires**: kubectl, cluster access
- **Interactive**: Yes
- **Estimated Duration**: Varies by action
