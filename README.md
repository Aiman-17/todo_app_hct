# AI TaskMaster - Intelligent Todo Application 🤖✨

A modern, full-stack todo application with **AI-powered branding** and **premium UI design**. Built progressively from console CLI to production-grade web application with authentication, advanced features, and beautiful user interface.

## Current Status: Phase IV - Kubernetes Deployment ✅

**Status**: ✅ **Phase IV Complete** | 🚀 **Phase V Planned** (Cloud K8s + Dapr + Kafka)
**Stack**: FastAPI + SQLModel + Neon PostgreSQL (backend) | Next.js 16+ + React 19 + TypeScript + Tailwind + shadcn/ui (frontend) | Google Gemini 2.0 Flash Lite (AI) | Kubernetes + Helm + Docker (Phase IV)
**Completion Date**: Phase IV - February 7, 2026
**Live Demos**:
- [Vercel Frontend](https://todo-app-hct-jb36.vercel.app/) (Phase III)
- [Vercel Backend](https://backend-gamma-six-76.vercel.app/) (Phase III)
- Codespaces K8s: GitHub Codespaces (Phase IV - development)

### 🎤 Voice Commands (NEW!)
Talk to your AI assistant using voice input:
- Click the microphone button in chat
- Speak naturally: "Add task buy groceries tomorrow"
- Automatic transcription and execution
- Works in Chrome, Edge, Safari (WebKit)
- Real-time visual feedback during recording

### 🌐 Multi-Language Support: Urdu (NEW!)
Get chatbot responses in Urdu:
- Toggle between English and اردو in the chat interface
- Full Urdu responses for all task operations
- Supports create, list, update, delete, complete tasks
- Native Urdu typography with proper font rendering
- Seamless language switching mid-conversation

### Phase II Quick Start

See [Phase II Quickstart Guide](specs/002-fullstack-web-auth/quickstart.md) for detailed setup.

**Backend** (http://localhost:8000):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure DATABASE_URL, BETTER_AUTH_SECRET
uvicorn src.main:app --reload
```

**Frontend** (http://localhost:3000, may auto-select 3001-3005 if port is in use):
```bash
cd frontend
npm install
cp .env.local.example .env.local  # Configure NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
npm run dev
```

> **Note**: Next.js will automatically find an available port if 3000 is in use. The backend CORS is pre-configured for ports 3000-3005.

### Phase II Features

**Backend (FastAPI)**:
- ✅ RESTful API with automatic OpenAPI/Swagger documentation
- ✅ JWT authentication (15-min access tokens, 7-day refresh tokens)
- ✅ User signup and login with bcrypt password hashing (12 rounds)
- ✅ PostgreSQL/SQLite database support with SQLModel ORM
- ✅ User isolation (users can only access their own tasks)
- ✅ Comprehensive logging and security headers
- ✅ CORS configuration for frontend integration
- ✅ Unit and integration tests with pytest
- ✅ Type-safe API with Pydantic validation

**Frontend (Next.js)**:
- ✅ Modern React 19 with Next.js 15 App Router
- ✅ Cookie-based authentication with automatic token management
- ✅ Responsive design (mobile, tablet, desktop) with 44px minimum touch targets
- ✅ Advanced keyboard navigation:
  - Press `N` to create new task
  - Press `/` to focus search
  - Press `F` to toggle filters
  - Press `Esc` to close modals/dropdowns
- ✅ Full accessibility (WCAG 2.1 Level AAA):
  - Screen reader support with ARIA live announcements
  - Semantic HTML with proper ARIA labels and roles
  - Keyboard-only navigation support
  - High contrast and focus indicators
- ✅ Real-time password validation
- ✅ Task CRUD operations (create, read, update, delete, toggle completion)
- ✅ Advanced filtering and search:
  - Debounced search (300ms) for optimal performance
  - Multi-select priority filters (high, medium, low)
  - Status filters (all, pending, completed)
  - Sort by: created date, due date, priority, last updated
- ✅ Smooth animations and transitions:
  - Fade-in and slide-in effects for task cards
  - Bounce animation on task completion
  - Skeleton loading states (no spinners)
- ✅ Settings page with tabbed interface:
  - Profile management (update name, change password)
  - Notifications preferences
  - Keyboard shortcuts reference
- ✅ Performance optimizations:
  - Code splitting with lazy loading for settings components
  - React.memo for preventing unnecessary re-renders
  - Debounced search to reduce API calls
- ✅ Toast notifications for user feedback
- ✅ Beautiful UI with shadcn/ui components and Tailwind CSS

### UI Enhancements (Phase II Extended)

**Modern AI-Branded Landing Page**:
- ✅ Custom navbar with Bot icon and AI TaskMaster branding
- ✅ Mobile-responsive hamburger menu with smooth transitions
- ✅ Hero section with 3D robot visualization (left side)
- ✅ Futuristic gradient background with animated particles
- ✅ AI-focused messaging: "Your AI Assistant for Effortless Productivity"
- ✅ Features showcase section with 6 key capabilities
- ✅ Stats section displaying user engagement metrics
- ✅ Call-to-action sections with prominent Get Started buttons
- ✅ Comprehensive footer with social links and navigation columns
- ✅ Custom animations:
  - `bounce-subtle`: Smooth 3D robot animation
  - `float`: Particle floating effects
  - `fade-in`: Smooth content appearance
  - `slide-in`: Content slide-in transitions

**Advanced Task Management**:
- ✅ Soft delete with undo functionality:
  - Tasks marked with `deleted_at` timestamp instead of hard deletion
  - Restore endpoint: `POST /api/tasks/{id}/restore`
  - Prevents accidental data loss
- ✅ Recurring tasks with recurrence rule selector:
  - Enable/disable checkbox for task repetition
  - Frequency dropdown: Daily, Weekly, Monthly, Yearly
  - Interval input: Repeat every N days/weeks/months/years
  - Full API support with `recurrence_rule` field
- ✅ Due date filtering dropdown:
  - Filter by: All, Today, Tomorrow, This Week, Overdue
  - Integrated into CommandBar filter panel
  - Real-time task list updates
- ✅ View mode persistence:
  - Grid/List view toggle saved to localStorage
  - User preference maintained across sessions
  - Smooth transitions between view modes

**Enhanced User Experience**:
- ✅ Debounced search (300ms) for optimal performance
- ✅ Skeleton loading states (no spinners) for better perceived performance
- ✅ Responsive design tested across mobile, tablet, and desktop breakpoints
- ✅ Accessibility-first approach with ARIA labels and keyboard shortcuts
- ✅ Toast notifications for all user actions (create, update, delete, restore)
- ✅ Context-aware UI states (loading, error, empty, success)

### Phase II Documentation
- [Spec](specs/002-fullstack-web-auth/spec.md) - Requirements and acceptance criteria
- [Plan](specs/002-fullstack-web-auth/plan.md) - Architecture and implementation strategy
- [Tasks](specs/002-fullstack-web-auth/tasks.md) - Complete task breakdown (230+ tasks including UI enhancements)
- [Quickstart](specs/002-fullstack-web-auth/quickstart.md) - 15-minute local setup guide
- [Backend README](backend/README.md) - Backend setup and API documentation
- [Frontend README](frontend/README.md) - Frontend setup and component architecture
- [Deployment Checklist](DEPLOYMENT.md) - Production deployment guide
- [Manual Testing Guide](MANUAL_TESTING.md) - 35+ test cases for manual QA
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI (when running)
- [ADRs](history/adr/) - Architecture Decision Records

---

## Phase IV: Kubernetes Deployment (Minikube + Helm) ✅

**Status**: ✅ **Complete** - Deployed to Minikube in GitHub Codespaces

### What Was Built

Phase IV transformed AI TaskMaster into a **cloud-native application** running on Kubernetes with:
- ✅ **Containerized Services**: Backend (FastAPI) and Frontend (Next.js) packaged as Docker images
- ✅ **Kubernetes Deployment**: Full stack deployed to Minikube via Helm charts
- ✅ **Service Mesh**: ClusterIP services with internal networking
- ✅ **Infrastructure Components**: Redis (state store) and Kafka (event streaming) deployed in-cluster
- ✅ **Health Checks**: Liveness and readiness probes for all services
- ✅ **Auto-Restart**: Kubernetes self-healing with automatic pod recovery

### Architecture

```
GitHub Codespaces
  ↓
Minikube (Local Kubernetes)
  ├── Namespace: ai-taskmaster
  ├── Backend Deployment (FastAPI) - 1 replica
  ├── Frontend Deployment (Next.js) - 1 replica
  ├── Redis Deployment (State Store) - 1 replica
  ├── Kafka Deployment (Event Streaming) - 1 replica
  └── Services (ClusterIP)
       ↓
External: Neon PostgreSQL (serverless)
```

### Quick Start (Phase IV)

**Prerequisites**:
- GitHub account with Codespaces access
- Git repository cloned to Codespaces

**Setup Commands** (Run in Codespaces terminal):

```bash
# 1. Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 2. Install kubectl (if not already installed)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 3. Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 4. Start Minikube
minikube start

# 5. Enable Ingress addon
minikube addons enable ingress

# 6. Build Docker images
docker build -t localhost/backend:1.1 ./backend
docker build -t localhost/frontend:1.1 ./frontend

# 7. Load images into Minikube
minikube image load localhost/backend:1.1
minikube image load localhost/frontend:1.1

# 8. Create secrets file
cat > deploy/values.secret.yaml << 'EOF'
secrets:
  databaseUrl: "YOUR_NEON_DATABASE_URL"
  betterAuthSecret: "YOUR_SECRET_KEY_MIN_32_CHARS"
  geminiApiKey: "YOUR_GEMINI_API_KEY"
EOF

# 9. Install Helm chart
helm install todo-app ./charts/todo-app -n ai-taskmaster --create-namespace -f deploy/values.secret.yaml

# 10. Wait for pods to be ready
kubectl wait --for=condition=ready pod --all -n ai-taskmaster --timeout=300s

# 11. Check deployment status
kubectl get pods -n ai-taskmaster
kubectl get svc -n ai-taskmaster

# 12. Port forward to access application
kubectl port-forward -n ai-taskmaster svc/frontend-service 3000:3000 &
kubectl port-forward -n ai-taskmaster svc/backend-service 8000:8000 &
```

**Access Application**:
- Frontend: Open forwarded port in Codespaces (usually auto-detected)
- Backend Health: `curl http://localhost:8000/api/health`

### Restart After Codespace Sleep

When your Codespace restarts or Minikube stops:

```bash
# Quick restart script
minikube start
kubectl wait --for=condition=ready pod --all -n ai-taskmaster --timeout=300s
kubectl get pods -n ai-taskmaster

# Restart port forwarding (if needed)
kubectl port-forward -n ai-taskmaster svc/frontend-service 3000:3000 &
kubectl port-forward -n ai-taskmaster svc/backend-service 8000:8000 &
```

### Demo Commands (For Judges/Reviewers)

```bash
# Show cluster status
minikube status
kubectl cluster-info

# Show all resources
kubectl get all -n ai-taskmaster

# Show Helm release
helm list -n ai-taskmaster
helm status todo-app -n ai-taskmaster

# Show pod details
kubectl describe pod -n ai-taskmaster -l app=todo-app

# Show logs
kubectl logs -n ai-taskmaster deploy/todo-backend --tail=50
kubectl logs -n ai-taskmaster deploy/todo-frontend --tail=50

# Test backend health
curl http://localhost:8000/api/health
```

### Phase IV Documentation

- [Spec](specs/004-k8s-minikube/spec.md) - Kubernetes deployment requirements
- [Plan](specs/004-k8s-minikube/plan.md) - Architecture and design decisions
- [Tasks](specs/004-k8s-minikube/tasks.md) - Implementation task breakdown
- [Quickstart](specs/004-k8s-minikube/quickstart.md) - Step-by-step deployment guide
- [Helm Charts](charts/todo-app/) - Kubernetes manifests and Helm configuration

---

## Phase V: Cloud Kubernetes + Dapr + Kafka (Planned) 🚀

**Status**: 📋 **Specification Complete** | 🔄 **Implementation Planned**

Phase V extends Phase IV to production-grade cloud infrastructure with advanced event-driven features.

### Planned Features

**Cloud Infrastructure**:
- ☐ Deploy to cloud Kubernetes (GKE/DOKS/AKS/OKE)
- ☐ Public HTTPS URLs with TLS certificates
- ☐ Auto-scaling (2-10 replicas based on load)
- ☐ Zero-downtime rolling updates

**Event-Driven Architecture (Kafka + Dapr)**:
- ☐ Redpanda Cloud integration (managed Kafka)
- ☐ Full Dapr stack:
  - Pub/Sub (Kafka abstraction)
  - State Management (PostgreSQL)
  - Cron Bindings (scheduled reminders)
  - Secrets Management (Kubernetes Secrets)
  - Service Invocation (mTLS)
- ☐ Event-driven workflows:
  - Task lifecycle events (create, update, complete, delete)
  - Automated reminders system
  - Recurring task engine
  - Real-time sync across clients
  - Audit log service

**Advanced Features**:
- ☐ Recurring tasks (Daily, Weekly, Monthly, Yearly)
- ☐ Due dates with smart reminders
- ☐ Task priorities (High, Medium, Low)
- ☐ Tags and categories
- ☐ Advanced search (full-text)
- ☐ Filters and sorting (by priority, due date, status)
- ☐ Real-time WebSocket updates

**CI/CD Pipeline**:
- ☐ GitHub Actions workflow
- ☐ Automated testing (unit, integration, E2E)
- ☐ Docker image builds and push to registry
- ☐ Automated deployment to staging
- ☐ Manual approval for production
- ☐ Smoke tests and health checks

**Observability**:
- ☐ Structured logging with correlation IDs
- ☐ Prometheus metrics
- ☐ Grafana dashboards
- ☐ Alerting (email/Slack)
- ☐ Distributed tracing

### Free Credits Available

All major cloud providers offer free credits for new users:
- **Google Cloud (GKE)**: $300 for 90 days
- **DigitalOcean (DOKS)**: $200 for 60 days
- **Azure (AKS)**: $200 for 30 days
- **Oracle Cloud (OKE)**: $300 for 30 days + Always Free tier

### Phase V Documentation

- [Spec](specs/005-cloud-k8s-dapr/spec.md) - Complete Phase V requirements and architecture
- [Plan](specs/005-cloud-k8s-dapr/plan.md) - Implementation strategy (To be created)
- [Tasks](specs/005-cloud-k8s-dapr/tasks.md) - Task breakdown (To be created)
- [Quickstart](specs/005-cloud-k8s-dapr/quickstart.md) - Cloud deployment guide (To be created)

---

## 🤖 Reusable Intelligence - AI Agent Architecture

AI TaskMaster implements a **modular, reusable AI agent system** using the **4-Agent Pipeline Pattern** for natural language processing. This architecture demonstrates **Reusable Intelligence** through Claude Code Subagents that can be extended, replaced, and reused across different contexts.

### Agent Architecture Overview

```
User Message → IntentClassifierAgent → TaskResolutionAgent → ActionAgent → ResponseFormatterAgent → Response
```

**Key Components**:

1. **IntentClassifierAgent** (`backend/src/agents/intent_classifier.py`)
   - Classifies user messages into structured intents (create, list, update, delete, complete)
   - Extracts entities (task title, priority, due date, tags)
   - Uses Google Gemini 2.0 Flash Lite with rule-based fallback
   - Handles typo normalization and low-confidence scenarios

2. **TaskResolutionAgent** (`backend/src/agents/task_resolution.py`)
   - Resolves ambiguous task references ("the grocery one", "first task")
   - Implements word-overlap fuzzy matching algorithm
   - Handles confirmation flow for multiple matches

3. **ActionAgent** (`backend/src/agents/action_agent.py`)
   - Routes intents to appropriate MCP tools
   - Executes CRUD operations with user isolation
   - Validates parameters and handles errors

4. **ResponseFormatterAgent** (`backend/src/agents/response_formatter.py`)
   - Formats responses in natural language
   - Provides context-aware, helpful messages
   - Supports emoji and structured metadata

### Why Reusable Intelligence?

✅ **Modular**: Each agent has a single, well-defined responsibility
✅ **Composable**: Agents can be combined in different pipelines
✅ **Portable**: Same agents work across web, CLI, mobile, voice
✅ **Extensible**: Easy to add capabilities without breaking existing code
✅ **Testable**: Each agent can be tested in isolation
✅ **Swappable**: Replace Gemini with OpenAI, Anthropic, etc.

### Example: Agent Reusability

```python
# Web API
@router.post("/chat")
async def chat(request: ChatRequest):
    service = ChatbotService()
    return service.process_message(db, user_id, request.message)

# CLI Application
def main():
    service = ChatbotService()  # Same agents!
    response = service.process_message(db, user_id, input("You: "))

# Slack Bot
@app.event("message")
def handle_message(event, say):
    service = ChatbotService()  # Same agents!
    say(service.process_message(db, event["user"], event["text"])["response"])
```

### Documentation

- 📚 [Agent Architecture](docs/agents-architecture.md) - Detailed technical architecture, agent responsibilities, and pipeline flow
- 🔧 [Reusable Intelligence Guide](docs/reusable-intelligence.md) - Design patterns, implementation examples, and best practices for reusing agents

### Agent Features

- **Natural Language Understanding**: "Buy milk", "I need to remember", "Show pending tasks"
- **Typo Tolerance**: "shw my tsks" → "show my tasks"
- **Fuzzy Task Matching**: "grocery" matches "Buy groceries at store"
- **Context-Aware**: Maintains conversation history for better understanding
- **Fallback Strategy**: Graceful degradation when AI API unavailable
- **Distributed Tracing**: Correlation IDs for debugging across agent pipeline

---

## 🎤 Voice Commands - Hands-Free Task Management

AI TaskMaster supports **voice input** for natural, hands-free task management using the **Web Speech API**.

### How It Works

```
User clicks mic → Browser Speech API → Transcription → Chat API → AI Response
```

**Features:**
- ✅ **Natural Speech Recognition**: Speak naturally, no keywords required
- ✅ **Auto-Send**: Transcribed text automatically sent to chatbot
- ✅ **Real-Time Feedback**: Visual indicators during recording
- ✅ **Error Handling**: Clear error messages for permissions, connectivity
- ✅ **Multi-Language**: Supports 11 languages (English, Spanish, French, German, Japanese, Chinese, Arabic, Urdu, etc.)
- ✅ **Browser Compatibility**: Chrome, Edge (full support), Safari (WebKit)

### Usage

1. **Click the microphone button** in the chat interface
2. **Grant microphone permission** (browser will prompt on first use)
3. **Speak your command**: "Add a high priority task to call the doctor tomorrow"
4. **Wait for transcription** (real-time visual feedback)
5. **Message auto-sends** and chatbot responds

### Example Voice Commands

| Command | Result |
|---------|--------|
| "Add task buy groceries" | Creates task: "buy groceries" |
| "Show my high priority tasks" | Lists all high priority tasks |
| "Mark task five as complete" | Completes task with ID 5 |
| "Delete the grocery task" | Deletes matching task |
| "What are my pending tasks" | Lists all incomplete tasks |

### Implementation Details

**Frontend Components:**
- `VoiceButton.tsx` - Microphone button with recording state
- `useSpeechRecognition.ts` - React hook for speech API
- `speech-recognition.ts` - Web Speech API wrapper with error handling

**Features:**
- **Permission Management**: Automatic permission request flow
- **Visual Feedback**: Pulsing animation during recording, listening indicator
- **Error Recovery**: Retry button for failed recordings
- **Graceful Fallback**: Hidden on unsupported browsers

**Browser Support:**
| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Best experience |
| Edge | ✅ Full | Same as Chrome |
| Safari | ✅ WebKit | Requires user interaction |
| Firefox | ⚠️ Limited | Requires about:config flag |

### Privacy & Security

- ✅ **No cloud storage**: Speech processed by browser, not stored
- ✅ **Permission-based**: Requires explicit microphone permission
- ✅ **User control**: Stop recording anytime
- ✅ **Local processing**: Transcription via browser's built-in API

---

## ☁️ Cloud-Native Blueprints - Kubernetes & Docker

AI TaskMaster is built with a **cloud-native architecture** supporting deployment across multiple environments using **Kubernetes**, **Docker Compose**, and **serverless platforms**.

### Architecture Overview

```
Load Balancer (NGINX Ingress)
    ↓
┌────────────────────────────────────────┐
│  Frontend (Next.js)  │  Backend (FastAPI) │
│  - 2 replicas        │  - 3 replicas       │
│  - Auto-scaling      │  - Auto-scaling     │
│  - Health checks     │  - Health checks    │
└────────────────────────────────────────┘
    ↓
Neon Serverless PostgreSQL
```

### Claude Code Agent Skills

Interactive automation skills for deployment and testing:

**`.claude-skills/deploy.md`** - Full deployment automation
- Pre-deployment checks (tests, linting, migrations)
- Environment-specific deployment (local/staging/production)
- Post-deployment verification and smoke tests
- Automatic rollback on failure

**`.claude-skills/test-chatbot.md`** - AI agent testing
- Unit tests for all 4 agents
- Integration tests for agent pipeline
- End-to-end conversation flow tests
- Performance testing (<5s SLA validation)

**`.claude-skills/k8s-deploy.md`** - Kubernetes helper
- Interactive deployment workflows
- Scaling operations (manual and auto-scaling)
- Troubleshooting guide for common issues
- Health monitoring and log management

### Kubernetes Deployment

**Production-ready manifests:**
```bash
kubernetes/
├── namespace.yaml           # Isolated namespace
├── backend-deployment.yaml  # 3 replicas, rolling updates
├── frontend-deployment.yaml # 2 replicas, auto-scaling
└── ingress.yaml             # SSL/TLS, load balancing
```

**Features:**
- ✅ **High Availability**: Multi-replica deployments (3 backend, 2 frontend)
- ✅ **Auto-Scaling**: HPA (2-10 replicas based on CPU)
- ✅ **Zero-Downtime**: Rolling updates with health checks
- ✅ **Self-Healing**: Automatic pod restart on failure
- ✅ **Load Balancing**: Traffic distribution across replicas
- ✅ **Resource Management**: CPU/memory limits and requests
- ✅ **Health Checks**: Liveness and readiness probes

**Quick Deploy:**
```bash
# Deploy to Kubernetes
kubectl apply -f kubernetes/

# Verify deployment
kubectl get pods -n ai-taskmaster
kubectl rollout status deployment/backend -n ai-taskmaster

# Access application
kubectl port-forward -n ai-taskmaster svc/frontend-service 3000:3000
```

### Docker Compose (Local Development)

**One-command setup:**
```bash
docker-compose up
```

**Services:**
- `postgres` - PostgreSQL 16 with health checks
- `backend` - FastAPI with hot-reload
- `frontend` - Next.js with hot-reload
- `nginx` - Reverse proxy (optional)

**Features:**
- ✅ Consistent development environment
- ✅ Hot module replacement (HMR)
- ✅ Volume mounting for live code changes
- ✅ Network isolation
- ✅ Health checks and dependencies

### Cloud-Native Patterns

**12-Factor App Compliance:**
- Codebase in version control
- Dependencies explicitly declared
- Config via environment variables
- Backing services as attached resources
- Stateless processes
- Port binding for services
- Horizontal scalability
- Fast startup and graceful shutdown
- Dev/prod parity
- Logs as event streams
- Admin processes as one-off tasks

**Container Security:**
- Minimal base images (python:3.13-slim, node:20-alpine)
- Non-root user execution
- Secret management via Kubernetes Secrets
- Image vulnerability scanning
- Network policies for pod isolation

**Observability:**
- Structured logging with correlation IDs
- Health check endpoints (/health)
- Metrics collection (CPU, memory, latency)
- Distributed tracing across agent pipeline
- Ready for Prometheus + Grafana

### Documentation

- 🏗️ [Cloud-Native Architecture](docs/cloud-native-architecture.md) - Complete system design, deployment strategies, monitoring, and disaster recovery
- 📦 [Kubernetes Manifests](kubernetes/) - Production-ready K8s configuration
- 🐳 [Docker Compose](docker-compose.yml) - Local development environment
- 🚀 [Deploy Skill](.claude-skills/deploy.md) - Automated deployment workflows
- ☸️ [K8s Deploy Skill](.claude-skills/k8s-deploy.md) - Interactive Kubernetes helper

### Deployment Targets

| Environment | Platform | Replicas | Resources | Cost |
|-------------|----------|----------|-----------|------|
| **Local** | Docker Compose | 1 each | Minimal | Free |
| **Staging** | Kubernetes | 2-5 | Medium | ~$50/mo |
| **Production** | Kubernetes | 3-10 | High | ~$200/mo |

---

## Deployment

### Quick Deployment to Vercel (Recommended)

**Prerequisites**:
- GitHub account
- Vercel account (free tier available)
- Neon PostgreSQL database (free tier available)

**Steps**:

1. **Prepare Environment Variables**:
   ```bash
   # Backend (.env)
   DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   CORS_ORIGINS=https://your-frontend-domain.vercel.app

   # Frontend (.env.local)
   NEXT_PUBLIC_API_URL=https://your-backend-domain.vercel.app
   BETTER_AUTH_SECRET=same-secret-as-backend
   BETTER_AUTH_URL=https://your-frontend-domain.vercel.app
   ```

2. **Deploy Backend** (FastAPI):
   - Push code to GitHub
   - Import project to Vercel
   - Select `backend` directory as root
   - Set build command: `pip install -r requirements.txt`
   - Set output directory: Leave empty (API routes)
   - Add environment variables in Vercel dashboard
   - Deploy and note the backend URL

3. **Deploy Frontend** (Next.js):
   - Import project to Vercel (separate deployment)
   - Select `frontend` directory as root
   - Framework preset: Next.js (auto-detected)
   - Add environment variables in Vercel dashboard
   - Update `NEXT_PUBLIC_API_URL` with backend URL from step 2
   - Deploy

4. **Update CORS**:
   - In Vercel backend settings, update `CORS_ORIGINS` environment variable
   - Add your frontend Vercel domain
   - Redeploy backend

**Alternative Deployment Options**:
- See [DEPLOYMENT.md](DEPLOYMENT.md) for Docker, Railway, Render, and self-hosted options
- [Manual Testing Guide](MANUAL_TESTING.md) for pre-deployment QA checklist

### Development vs Production

**Development Mode** (Current setup):
- Backend: `uvicorn src.main:app --reload` on port 8000
- Frontend: `npm run dev` on port 3000-3005 (auto-selects available port)
- Hot module reloading enabled
- Debug logging active
- SQLite/Neon PostgreSQL supported

**Production Mode**:
- Backend: Uvicorn with workers, no `--reload` flag
- Frontend: `npm run build && npm start` (SSR required, not static export)
- Optimized builds with minification
- Production logging (errors only)
- PostgreSQL required (Neon recommended)
- Environment variables must be set securely
- HTTPS required for authentication cookies

**Important Notes**:
- ⚠️ This app requires **Server-Side Rendering (SSR)** due to client-side authentication
- ❌ Static export (`output: 'export'`) is NOT supported
- ✅ Vercel, Netlify (SSR), Docker with Node.js, Railway, Render all work
- ❌ GitHub Pages, S3 static hosting will NOT work

---

## Phase I: Console Application ✅

A simple, in-memory Python console application for managing todo tasks.

## Features

- ✅ Add tasks with title and optional description
- ✅ View all tasks with completion status
- ✅ Update task title and description
- ✅ Delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Exit confirmation to prevent accidental data loss

## Requirements

- Python 3.13 or higher
- No external dependencies (standard library only)

## Complete Setup Guide (For Future Development)

This guide helps you set up the entire project from scratch after cloning the repository. Perfect for contributing, forking, or continuing development.

### Prerequisites

**System Requirements**:
- **Python**: 3.13+ (backend)
- **Node.js**: 20 LTS (frontend)
- **Git**: Latest version
- **Docker**: Latest version (for Phase IV/V)

**Cloud Accounts** (Optional - for Phase IV/V):
- **Neon PostgreSQL**: Free serverless database (https://neon.tech)
- **Google Gemini API**: Free tier (https://ai.google.dev)
- **GitHub Account**: For Codespaces and CI/CD
- **Cloud Provider** (Phase V only): GKE/DOKS/AKS/OKE with free credits

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/todo_app_hct.git
cd todo_app_hct
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL: Your Neon PostgreSQL connection string
# - BETTER_AUTH_SECRET: Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
# - GEMINI_API_KEY: Your Google Gemini API key
# - CORS_ORIGINS: http://localhost:3000,http://localhost:3001 (add more ports if needed)
# - ENVIRONMENT: development

# Run database migrations (if any)
# alembic upgrade head

# Start backend
uvicorn src.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local with your credentials:
# - NEXT_PUBLIC_API_URL: http://localhost:8000 (backend URL)
# - BETTER_AUTH_SECRET: Same as backend
# - BETTER_AUTH_URL: http://localhost:3000 (or auto-selected port)

# Start frontend (development mode)
npm run dev
```

Frontend will be available at: http://localhost:3000 (or 3001-3005 if 3000 is in use)

### Step 4: Verify Installation

1. **Open Frontend**: Navigate to http://localhost:3000
2. **Sign Up**: Create a new account
3. **Create Task**: Add a test task via UI or chatbot
4. **Test Chatbot**: Type "show my tasks" in the chat interface
5. **Test Voice**: Click microphone button (Chrome/Edge only) and say "Add task test voice"

### Step 5: Phase IV Kubernetes Setup (Optional)

**Option A: GitHub Codespaces** (Recommended - No local setup needed)

```bash
# 1. Open repository in GitHub Codespaces
# 2. Codespaces comes with Docker, kubectl, and Minikube pre-installed
# 3. Follow Phase IV Quick Start commands from README
```

**Option B: Local Kubernetes** (Docker Desktop required)

```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Enable Kubernetes in Docker Desktop settings
# OR install Minikube:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe
# Install and add to PATH

# Install kubectl
curl -LO "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
# Add to PATH

# Install Helm
choco install kubernetes-helm
# OR download from: https://helm.sh/docs/intro/install/

# Follow Phase IV Quick Start commands
minikube start
# ... (see Phase IV section)
```

### Step 6: Development Tools (Recommended)

```bash
# Install Claude Code CLI (for AI-assisted development)
# Instructions: https://github.com/anthropics/claude-code

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Install ESLint and Prettier (frontend)
cd frontend
npm install --save-dev eslint prettier

# Install Python linters (backend)
cd backend
pip install black mypy ruff
```

### Common Issues & Solutions

**Issue: Port 3000 already in use**
- Solution: Next.js auto-selects 3001-3005. Update CORS_ORIGINS in backend .env

**Issue: Database connection failed**
- Solution: Verify DATABASE_URL in .env, check Neon dashboard for connection string

**Issue: Chatbot not responding**
- Solution: Verify GEMINI_API_KEY is set, check backend logs for errors

**Issue: Docker build fails**
- Solution: Ensure package-lock.json exists (run `npm install` in frontend)

**Issue: Minikube won't start**
- Solution: Check Docker is running, try `minikube delete && minikube start`

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd todo_app_hct

# Verify Python version
python --version  # Should show Python 3.13.x or higher
```

## Running the Application

```bash
# Navigate to the src directory
cd src

# Run the application
python main.py
```

## Usage

The application presents a numbered menu with 6 options:

```
=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

### Example Session

```bash
$ cd src
$ python main.py

=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6): 1
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task #1 created: Buy groceries

Enter choice (1-6): 2

Your Tasks:
[ ] 1. Buy groceries - Milk, eggs, bread

Legend:
[ ] = Incomplete
[✓] = Complete

Enter choice (1-6): 5
Enter task ID: 1

✓ Task #1 marked as complete

Enter choice (1-6): 6

Exit? All tasks will be lost. [Y/N]: Y

Goodbye!
```

## Important Notes

⚠️ **Data is not persisted!** All tasks are stored in memory and will be lost when you exit the application. This is intentional for Phase I.

## Project Structure

```
todo_app_hct/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic & CRUD operations
│   └── cli/
│       ├── __init__.py
│       └── menu.py           # CLI interface handlers
├── specs/                    # Specifications and planning docs
├── tests/                    # Test directory (future use)
└── README.md
```

## Development

This project follows spec-driven development principles. See `specs/001-phase1-console/` for:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `tasks.md` - Task breakdown
- `data-model.md` - Data structures
- `contracts/cli-interface.md` - CLI specifications

## Roadmap

- **Phase I**: ✅ Console CLI (In-memory storage) - **Complete**
- **Phase II**: ✅ Full-Stack Web App (JWT auth, PostgreSQL, REST API, Next.js, Responsive UI) - **Complete**
- **Phase III**: ✅ AI Chatbot + Voice Commands (Google Gemini, MCP, Web Speech API) - **Complete**
- **Phase IV**: ✅ Local Kubernetes Deployment (Minikube + Helm + Docker in GitHub Codespaces) - **Complete**
- **Phase V**: 📋 Cloud Kubernetes + Dapr + Kafka (GKE/DOKS/AKS/OKE, Redpanda Cloud, Event-Driven Architecture) - **Planned**

### Future Enhancements (Post-Hackathon)

After completing Phase V, planned improvements include:
- 📱 **Mobile App**: React Native app with offline support
- 🔔 **Push Notifications**: Real-time reminders via Firebase/OneSignal
- 🤝 **Team Collaboration**: Shared tasks, assignments, and comments
- 🎤 **Voice Reminders**: AI-powered voice notifications for due tasks
- 📊 **Analytics Dashboard**: Task completion trends and productivity insights
- 🌐 **Multi-Language**: Support for 20+ languages
- 🎨 **Themes**: Dark mode, custom color schemes
- 🔌 **Integrations**: Google Calendar, Slack, Microsoft Teams
- 🧠 **AI Prioritization**: Smart task ranking based on context and history

## Contributing

Contributions are welcome! This project is actively maintained and improved post-hackathon.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the spec-driven development process**:
   - Create spec: `specs/<feature-name>/spec.md`
   - Create plan: `specs/<feature-name>/plan.md`
   - Create tasks: `specs/<feature-name>/tasks.md`
4. **Implement the feature**: Follow Phase structure (console → web → AI → K8s)
5. **Write tests**: Unit tests (backend/frontend), integration tests
6. **Update documentation**: README.md, API docs, quickstart guides
7. **Commit your changes**: `git commit -m 'Add amazing feature'`
8. **Push to branch**: `git push origin feature/amazing-feature`
9. **Create Pull Request**: Reference the spec and completed tasks

### Contribution Guidelines

- **Code Quality**: Follow existing patterns, use type hints (Python), TypeScript strict mode
- **Testing**: Minimum 80% coverage for new code
- **Documentation**: Update README, add JSDoc/docstrings, create runbooks if needed
- **Commits**: Use conventional commits (feat:, fix:, docs:, etc.)
- **Specs**: All new features require spec → plan → tasks workflow

### Areas for Contribution

**High Priority** (Post-Hackathon):
- [ ] Complete Phase V (Cloud K8s + Dapr + Kafka)
- [ ] Implement recurring tasks engine
- [ ] Add smart reminders with Dapr Cron Bindings
- [ ] Build real-time WebSocket sync
- [ ] Set up CI/CD pipeline with GitHub Actions

**Medium Priority**:
- [ ] Add task priorities and tags
- [ ] Implement advanced search with filters
- [ ] Create notification service (email/push)
- [ ] Add audit log service (Kafka consumer)
- [ ] Improve chatbot NLP (multi-turn conversations)

**Nice to Have**:
- [ ] Mobile app (React Native)
- [ ] Dark mode with theme switcher
- [ ] Calendar integration (Google Calendar)
- [ ] Team collaboration features
- [ ] Productivity analytics dashboard

---

## Portfolio Use

This project demonstrates:

✅ **Full-Stack Development**:
- Modern Python backend (FastAPI, SQLModel, async/await)
- Modern React frontend (Next.js 16, React 19, TypeScript, Tailwind)
- RESTful API design with OpenAPI documentation
- JWT authentication with secure token handling

✅ **AI/ML Integration**:
- Google Gemini 2.0 Flash integration
- Natural language processing for task management
- Voice-to-text with Web Speech API
- 4-agent pipeline architecture (Intent → Resolution → Action → Response)

✅ **Cloud-Native Architecture**:
- Docker containerization (multi-stage builds)
- Kubernetes deployment (Minikube → Cloud K8s)
- Helm charts for infrastructure as code
- Service mesh with Dapr sidecars

✅ **Event-Driven Design**:
- Kafka for asynchronous event streaming
- Pub/Sub patterns with Dapr
- Real-time WebSocket updates
- Microservices architecture (Notification, Recurring Tasks, Audit services)

✅ **DevOps & CI/CD**:
- GitHub Actions workflows
- Automated testing (unit, integration, E2E)
- Docker image builds and registry
- Zero-downtime deployments

✅ **Best Practices**:
- Spec-driven development (SDD)
- Test-driven development (TDD)
- SOLID principles
- 12-Factor App compliance
- Comprehensive documentation

### Showcasing This Project

**For Recruiters**:
- Highlight the **end-to-end ownership**: Spec → Design → Implementation → Deployment
- Emphasize **production-ready code**: Authentication, error handling, logging, monitoring
- Showcase **modern tech stack**: Latest versions of FastAPI, Next.js, React, Kubernetes

**For Technical Interviews**:
- Discuss **architecture decisions**: Why Dapr? Why Kafka? Why Kubernetes?
- Explain **trade-offs**: SSR vs SSG, Minikube vs Cloud, REST vs GraphQL
- Walk through **agent pipeline**: How NLP intent classification works

**For Portfolio Website**:
- Include **live demo links**: Vercel deployment URLs
- Add **architecture diagrams**: System design, agent flow, Kubernetes topology
- Showcase **code snippets**: Agent implementation, Dapr integration, Helm charts

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## Acknowledgments

- **Hackathon**: Built for Spec-Driven Development Hackathon II
- **Technologies**: FastAPI, Next.js, React, PostgreSQL, Kubernetes, Dapr, Kafka, Google Gemini
- **Tools**: Claude Code, GitHub Codespaces, Neon, Vercel, Redpanda Cloud
- **Inspiration**: Modern productivity apps, event-driven architecture, AI-powered assistants

---

## Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/YOUR_USERNAME/todo_app_hct/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/YOUR_USERNAME/todo_app_hct/discussions)
- **Email**: aurex707@gmail.com

---

**⭐ Star this repo if you find it useful!**
