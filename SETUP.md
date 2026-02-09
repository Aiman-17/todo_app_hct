# Complete Setup Reference Guide

This document provides a comprehensive reference for all dependencies, packages, and installation commands needed to set up AI TaskMaster from scratch.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Backend Dependencies](#backend-dependencies)
3. [Frontend Dependencies](#frontend-dependencies)
4. [Phase IV - Kubernetes Tools](#phase-iv---kubernetes-tools)
5. [Phase V - Cloud Tools](#phase-v---cloud-tools)
6. [Development Tools](#development-tools)
7. [Environment Variables](#environment-variables)
8. [Quick Start Commands](#quick-start-commands)

---

## System Requirements

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Python** | 3.13+ | Backend runtime | https://www.python.org/downloads/ |
| **Node.js** | 20 LTS | Frontend runtime | https://nodejs.org/ |
| **npm** | 10+ | Package manager | Comes with Node.js |
| **Git** | Latest | Version control | https://git-scm.com/ |
| **Docker** | Latest | Containerization | https://www.docker.com/products/docker-desktop |

---

## Backend Dependencies

### Core Packages (requirements.txt)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Package Breakdown

**Web Framework**:
```bash
fastapi==0.109.0           # Modern async web framework
uvicorn[standard]==0.27.0  # ASGI server with uvloop
starlette==0.35.1          # FastAPI's foundation
```

**Database & ORM**:
```bash
sqlmodel==0.0.14                 # SQLAlchemy + Pydantic ORM
psycopg[binary]>=3.1.0           # PostgreSQL driver (async)
alembic==1.13.1                  # Database migrations
```

**Authentication**:
```bash
pyjwt==2.8.0                     # JSON Web Tokens
bcrypt==4.1.2                    # Password hashing
cryptography==46.0.4             # Encryption utilities
```

**Validation & Data**:
```bash
pydantic==2.12.5                 # Data validation
pydantic-core==2.41.5            # Pydantic core
email-validator==2.3.0           # Email validation
```

**AI Integration**:
```bash
google-generativeai==0.8.6       # Google Gemini API
google-ai-generativelanguage     # Gemini types
```

**Testing**:
```bash
pytest==9.0.2                    # Test framework
pytest-asyncio==1.3.0            # Async test support
```

**Utilities**:
```bash
python-dotenv==1.0.0             # Environment variables
httpx==0.28.1                    # Async HTTP client
```

---

## Frontend Dependencies

### Core Packages (package.json)

```bash
# Navigate to frontend directory
cd frontend

# Install all dependencies
npm install
```

### Package Breakdown

**React & Next.js**:
```bash
npm install next@15.5.12           # Next.js framework
npm install react@19.0.0           # React library
npm install react-dom@19.0.0       # React DOM
```

**TypeScript**:
```bash
npm install --save-dev typescript@5.7.3
npm install --save-dev @types/node
npm install --save-dev @types/react
npm install --save-dev @types/react-dom
```

**Styling**:
```bash
npm install tailwindcss@3.5.1           # Utility-first CSS
npm install postcss                      # CSS processing
npm install autoprefixer                 # CSS vendor prefixes
npm install @tailwindcss/typography      # Typography plugin
npm install tailwind-merge               # Merge Tailwind classes
npm install clsx                         # Conditional classnames
```

**UI Components** (shadcn/ui):
```bash
# shadcn/ui components are added via CLI:
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add select
npx shadcn@latest add toast
npx shadcn@latest add skeleton
npx shadcn@latest add tabs
```

**Icons**:
```bash
npm install lucide-react               # Icon library
```

**State Management & Forms**:
```bash
npm install zustand                    # State management
npm install react-hook-form            # Form handling
npm install @hookform/resolvers        # Form validation
npm install zod                        # Schema validation
```

**Date & Time**:
```bash
npm install date-fns                   # Date utilities
```

**HTTP Client**:
```bash
npm install axios                      # HTTP requests (alternative to fetch)
```

**Linting**:
```bash
npm install --save-dev eslint          # Linter
npm install --save-dev eslint-config-next  # Next.js ESLint config
```

---

## Phase IV - Kubernetes Tools

### Minikube

**Windows**:
```bash
# Download installer
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe

# Run installer (or use Chocolatey)
choco install minikube
```

**macOS**:
```bash
brew install minikube
```

**Linux**:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### kubectl

**Windows**:
```bash
curl -LO "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
# Add to PATH
```

**macOS**:
```bash
brew install kubectl
```

**Linux**:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Helm

**All Platforms**:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Windows (Chocolatey)**:
```bash
choco install kubernetes-helm
```

**macOS**:
```bash
brew install helm
```

### Docker

Download Docker Desktop:
- Windows/macOS: https://www.docker.com/products/docker-desktop
- Linux: Use Docker Engine + Docker Compose

---

## Phase V - Cloud Tools

### Google Cloud SDK (gcloud)

**All Platforms**:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

**Windows (Installer)**:
- Download from: https://cloud.google.com/sdk/docs/install

### DigitalOcean CLI (doctl)

**macOS/Linux**:
```bash
brew install doctl

# OR
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.104.0/doctl-1.104.0-linux-amd64.tar.gz
tar xf ~/doctl-1.104.0-linux-amd64.tar.gz
sudo mv ~/doctl /usr/local/bin
```

### Azure CLI (az)

**Windows**:
```bash
# Download installer
https://aka.ms/installazurecliwindows
```

**macOS**:
```bash
brew install azure-cli
```

**Linux**:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Oracle Cloud CLI (oci)

**All Platforms**:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

### Dapr CLI

**Windows**:
```powershell
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
```

**macOS/Linux**:
```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

---

## Development Tools

### Code Quality Tools

**Backend (Python)**:
```bash
pip install black           # Code formatter
pip install mypy            # Static type checker
pip install ruff            # Fast linter
pip install pre-commit      # Git hooks
```

**Frontend (Node.js)**:
```bash
npm install --save-dev prettier                    # Code formatter
npm install --save-dev eslint                      # Linter
npm install --save-dev @typescript-eslint/parser   # TS parser
npm install --save-dev @typescript-eslint/eslint-plugin  # TS rules
```

### Testing Tools

**Backend**:
```bash
pip install pytest                    # Test framework
pip install pytest-asyncio            # Async tests
pip install pytest-cov                # Coverage reports
pip install httpx                     # Test client
```

**Frontend**:
```bash
npm install --save-dev @testing-library/react
npm install --save-dev @testing-library/jest-dom
npm install --save-dev jest
npm install --save-dev jest-environment-jsdom
```

### Database Tools

**PostgreSQL Client** (Optional):
```bash
# macOS
brew install postgresql

# Windows (via Chocolatey)
choco install postgresql

# Linux (Ubuntu/Debian)
sudo apt install postgresql-client
```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+psycopg://username:password@host:5432/database?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long

# AI Integration
GEMINI_API_KEY=your-google-gemini-api-key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005

# Environment
ENVIRONMENT=development
```

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication
BETTER_AUTH_SECRET=same-as-backend-secret
BETTER_AUTH_URL=http://localhost:3000
```

### Kubernetes Secrets (Phase IV/V)

```yaml
# deploy/values.secret.yaml
secrets:
  databaseUrl: "postgresql+psycopg://username:password@host:5432/database?sslmode=require"
  betterAuthSecret: "your-secret-key-min-32-characters-long"
  geminiApiKey: "your-google-gemini-api-key"
```

---

## Quick Start Commands

### Complete Fresh Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/todo_app_hct.git
cd todo_app_hct

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn src.main:app --reload

# 3. Frontend setup (new terminal)
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your credentials
npm run dev

# 4. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Kubernetes Setup (Phase IV)

```bash
# 1. Install tools (if not already installed)
# See sections above for installation commands

# 2. Start Minikube
minikube start
minikube addons enable ingress

# 3. Build and load images
docker build -t localhost/backend:1.1 ./backend
docker build -t localhost/frontend:1.1 ./frontend
minikube image load localhost/backend:1.1
minikube image load localhost/frontend:1.1

# 4. Create secrets
cat > deploy/values.secret.yaml << 'EOF'
secrets:
  databaseUrl: "YOUR_DATABASE_URL"
  betterAuthSecret: "YOUR_SECRET"
  geminiApiKey: "YOUR_API_KEY"
EOF

# 5. Deploy with Helm
helm install todo-app ./charts/todo-app -n ai-taskmaster --create-namespace -f deploy/values.secret.yaml

# 6. Wait for pods
kubectl wait --for=condition=ready pod --all -n ai-taskmaster --timeout=300s

# 7. Access application
kubectl port-forward -n ai-taskmaster svc/frontend-service 3000:3000 &
kubectl port-forward -n ai-taskmaster svc/backend-service 8000:8000 &
```

### Restart After Codespace Sleep

```bash
# Quick restart
minikube start
kubectl wait --for=condition=ready pod --all -n ai-taskmaster --timeout=300s
kubectl get pods -n ai-taskmaster
```

---

## Troubleshooting

### Backend Won't Start

**Error: Database connection failed**
```bash
# Check DATABASE_URL format
# Should be: postgresql+psycopg://user:pass@host:5432/dbname?sslmode=require

# Test connection
python -c "from sqlmodel import create_engine; engine = create_engine('YOUR_DATABASE_URL'); print('✅ Connected')"
```

**Error: Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Start

**Error: Port 3000 in use**
```bash
# Next.js will auto-select 3001-3005
# Update backend CORS_ORIGINS to include the new port
```

**Error: Cannot find module**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Minikube Issues

**Error: Minikube won't start**
```bash
# Delete and recreate
minikube delete
minikube start --driver=docker

# Check Docker is running
docker ps
```

**Error: Pods stuck in Pending**
```bash
# Check events
kubectl get events -n ai-taskmaster --sort-by='.lastTimestamp'

# Check resources
kubectl describe pod -n ai-taskmaster <pod-name>
```

---

## Additional Resources

- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Phase IV Quickstart**: [specs/004-k8s-minikube/quickstart.md](specs/004-k8s-minikube/quickstart.md)
- **Phase V Spec**: [specs/005-cloud-k8s-dapr/spec.md](specs/005-cloud-k8s-dapr/spec.md)
- **API Documentation**: http://localhost:8000/docs (when running)

---

**Need Help?** Open an issue on GitHub or check the documentation links above.
