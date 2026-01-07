# AI TaskMaster - Intelligent Todo Application 🤖✨

A modern, full-stack todo application with **AI-powered branding** and **premium UI design**. Built progressively from console CLI to production-grade web application with authentication, advanced features, and beautiful user interface.

## Current Status: Phase II + UI Enhancements ✅

**Status**: ✅ **Complete** (230+ tasks - Core features + Premium UI)
**Stack**: FastAPI + SQLModel + Neon PostgreSQL (backend) | Next.js 16+ + React 19 + TypeScript + Tailwind + shadcn/ui (frontend)
**Completion Date**: January 6, 2026
**Live Demo**: [AI TaskMaster](http://localhost:3005) (Development)

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
