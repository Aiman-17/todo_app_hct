# Deploy - Application Deployment Automation Skill

## Description
Automated deployment skill for AI TaskMaster application. Handles deployment to local (Minikube), staging, and production environments with pre-deployment checks and post-deployment verification.

## Usage
```
/deploy [environment] [--skip-tests] [--skip-migration]
```

**Parameters:**
- `environment`: Target environment (local|staging|production)
- `--skip-tests`: Skip test suite execution (not recommended)
- `--skip-migration`: Skip database migrations (not recommended)

**Examples:**
```bash
/deploy local                    # Deploy to Minikube
/deploy staging                  # Deploy to staging environment
/deploy production               # Deploy to production (requires approval)
/deploy local --skip-tests       # Quick local deploy without tests
```

## Pre-Deployment Checklist

Before deploying, this skill verifies:

✅ **Code Quality**
- [ ] All tests passing (`pytest backend/tests/`)
- [ ] No linting errors (`ruff check`)
- [ ] No type errors (`mypy backend/src/`)

✅ **Environment Configuration**
- [ ] Environment variables configured (.env files present)
- [ ] Database connection string valid
- [ ] API keys present (GEMINI_API_KEY, BETTER_AUTH_SECRET)
- [ ] CORS origins configured correctly

✅ **Database**
- [ ] Migrations up to date (`alembic current`)
- [ ] Database backup created (production only)
- [ ] Connection pool settings optimized

✅ **Dependencies**
- [ ] Backend requirements.txt up to date
- [ ] Frontend package.json dependencies installed
- [ ] No security vulnerabilities (`npm audit`, `pip-audit`)

## Deployment Flow

### Local Deployment (Minikube)

```bash
# 1. Build Docker images
docker build -t ai-taskmaster-backend:latest ./backend
docker build -t ai-taskmaster-frontend:latest ./frontend

# 2. Load images to Minikube
minikube image load ai-taskmaster-backend:latest
minikube image load ai-taskmaster-frontend:latest

# 3. Apply Kubernetes manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

# 4. Wait for rollout
kubectl rollout status deployment/backend -n ai-taskmaster
kubectl rollout status deployment/frontend -n ai-taskmaster

# 5. Run migrations
kubectl exec -n ai-taskmaster deployment/backend -- alembic upgrade head

# 6. Verify health
kubectl get pods -n ai-taskmaster
curl $(minikube service frontend -n ai-taskmaster --url)/api/health
```

### Staging/Production Deployment

```bash
# 1. Tag and push images to registry
docker tag ai-taskmaster-backend:latest registry.example.com/ai-taskmaster-backend:v1.2.3
docker tag ai-taskmaster-frontend:latest registry.example.com/ai-taskmaster-frontend:v1.2.3
docker push registry.example.com/ai-taskmaster-backend:v1.2.3
docker push registry.example.com/ai-taskmaster-frontend:v1.2.3

# 2. Update Kubernetes manifests with new image tags
sed -i 's|image: .*backend.*|image: registry.example.com/ai-taskmaster-backend:v1.2.3|' kubernetes/backend-deployment.yaml
sed -i 's|image: .*frontend.*|image: registry.example.com/ai-taskmaster-frontend:v1.2.3|' kubernetes/frontend-deployment.yaml

# 3. Apply changes with rolling update
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml

# 4. Monitor rollout
kubectl rollout status deployment/backend -n ai-taskmaster
kubectl rollout status deployment/frontend -n ai-taskmaster

# 5. Run smoke tests
./scripts/smoke-tests.sh staging
```

## Post-Deployment Verification

After deployment, verify:

✅ **Health Checks**
```bash
# Backend health
curl https://api.example.com/health
# Expected: {"status": "healthy", "database": "connected"}

# Frontend health
curl https://app.example.com/
# Expected: 200 OK with HTML content
```

✅ **Database Connectivity**
```bash
# Check database connection
kubectl exec -n ai-taskmaster deployment/backend -- python -c "from src.config import settings; from sqlmodel import create_engine; engine = create_engine(settings.DATABASE_URL); engine.connect()"
```

✅ **API Endpoints**
```bash
# Test authentication
curl -X POST https://api.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Test task listing (requires auth token)
curl -X GET https://api.example.com/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

✅ **Chat Functionality**
```bash
# Test chatbot endpoint
curl -X POST https://api.example.com/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"show my tasks"}'
```

## Rollback Procedure

If deployment fails or issues detected:

```bash
# 1. Rollback to previous version
kubectl rollout undo deployment/backend -n ai-taskmaster
kubectl rollout undo deployment/frontend -n ai-taskmaster

# 2. Verify rollback successful
kubectl rollout status deployment/backend -n ai-taskmaster
kubectl rollout status deployment/frontend -n ai-taskmaster

# 3. Notify team
echo "Deployment rolled back. Investigating issues..."

# 4. Check logs for errors
kubectl logs -n ai-taskmaster deployment/backend --tail=100
kubectl logs -n ai-taskmaster deployment/frontend --tail=100
```

## Environment-Specific Configuration

### Local (Minikube)
- Database: PostgreSQL in-cluster
- Ingress: Minikube tunnel
- Replicas: 1 backend, 1 frontend
- Resources: Minimal (256Mi memory, 0.1 CPU)

### Staging
- Database: Neon Serverless PostgreSQL
- Ingress: NGINX Ingress Controller
- Replicas: 2 backend, 2 frontend
- Resources: Medium (512Mi memory, 0.5 CPU)
- Auto-scaling: HPA enabled (min: 2, max: 5)

### Production
- Database: Neon Serverless PostgreSQL (dedicated)
- Ingress: NGINX + Cloudflare
- Replicas: 3 backend, 3 frontend
- Resources: High (1Gi memory, 1 CPU)
- Auto-scaling: HPA enabled (min: 3, max: 10)
- Monitoring: Prometheus + Grafana
- Logging: ELK Stack

## Troubleshooting

### Pods not starting
```bash
# Check pod status
kubectl get pods -n ai-taskmaster

# Check pod logs
kubectl logs -n ai-taskmaster <pod-name>

# Describe pod for events
kubectl describe pod -n ai-taskmaster <pod-name>

# Common issues:
# - ImagePullBackOff: Check image name/tag and registry credentials
# - CrashLoopBackOff: Check application logs and environment variables
# - Pending: Check resource availability and node capacity
```

### Database connection issues
```bash
# Verify database secret
kubectl get secret -n ai-taskmaster postgres-secret -o yaml

# Test connection from pod
kubectl exec -n ai-taskmaster deployment/backend -- python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"

# Check network policies
kubectl get networkpolicies -n ai-taskmaster
```

### Service not accessible
```bash
# Check service endpoints
kubectl get endpoints -n ai-taskmaster

# Check ingress configuration
kubectl get ingress -n ai-taskmaster
kubectl describe ingress -n ai-taskmaster

# Test service from within cluster
kubectl run -n ai-taskmaster curl --image=curlimages/curl -it --rm -- curl http://backend-service:8000/health
```

## Metrics & Monitoring

Post-deployment, monitor these metrics:

- **Response Time**: p50, p95, p99 latency for API endpoints
- **Error Rate**: 4xx and 5xx error percentage
- **CPU Usage**: Backend pod CPU utilization
- **Memory Usage**: Backend pod memory utilization
- **Database Connections**: Active connection count
- **Chat Requests**: Requests per minute to /api/chat

**Alert Thresholds:**
- Error rate > 5%: Warning
- Error rate > 10%: Critical
- Response time p95 > 5s: Warning
- CPU usage > 80%: Warning
- Memory usage > 90%: Critical

## Success Criteria

Deployment is successful when:

✅ All pods in `Running` state
✅ All health checks passing
✅ Database migrations applied successfully
✅ Smoke tests passing (login, list tasks, create task, chat)
✅ No error spikes in logs
✅ Response times within SLA (<5s p95)
✅ Zero downtime (rolling update)

## Related Documentation

- [Kubernetes Manifests](../kubernetes/) - K8s configuration files
- [Docker Compose](../docker-compose.yml) - Local development setup
- [Cloud-Native Architecture](../docs/cloud-native-architecture.md) - System design
- [Deployment Checklist](../DEPLOYMENT.md) - Production deployment guide

## Skill Metadata

- **Type**: Automation
- **Category**: DevOps, Deployment
- **Complexity**: High
- **Requires**: kubectl, docker, minikube (for local)
- **Estimated Duration**: 5-15 minutes depending on environment
- **Rollback Support**: Yes (kubectl rollout undo)
