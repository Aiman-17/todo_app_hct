# AI TaskMaster - Intelligent Todo Application 🤖✨

A modern, full-stack todo application with **AI-powered branding** and **premium UI design**. Built progressively from console CLI to production-grade web application with authentication, advanced features, and beautiful user interface.

## Current Status: Phase III - AI Chatbot + Voice Commands ✅

**Status**: ✅ **Complete** (310+ tasks - Core features + Premium UI + AI Chatbot + Voice Commands)
**Stack**: FastAPI + SQLModel + Neon PostgreSQL (backend) | Next.js 16+ + React 19 + TypeScript + Tailwind + shadcn/ui (frontend) | Google Gemini 2.0 Flash Lite (AI)
**Completion Date**: January 30, 2026
**Live Demo**: [AI TaskMaster](http://localhost:3005) (Development)

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

## Installation

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
- **Phase III**: 🎯 AI chatbot interface (OpenAI Agents + MCP) - **Next Phase**
- **Phase IV**: Local Kubernetes deployment (Minikube + Dapr + Kafka)
- **Phase V**: Cloud deployment (DOKS/GKE/AKS)

## License

[Add your license here]
