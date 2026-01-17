# Quickstart Guide: Phase III AI Chatbot

**Target Audience**: Developers implementing or extending Phase III
**Prerequisites**: Phase II completed (backend + frontend + authentication)
**Time to Complete**: 30-45 minutes

## Overview

This guide walks you through setting up the Phase III AI Chatbot development environment and running your first conversational task management flow.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Migration](#database-migration)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Testing the Integration](#testing-the-integration)
7. [Development Workflow](#development-workflow)
8. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### System Requirements
- Python 3.13+ (backend)
- Node.js 20+ (frontend)
- PostgreSQL 14+ (Neon Serverless recommended)
- Git (for version control)

### Phase II Completion Check
Verify Phase II is working:
```bash
# Backend health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Frontend running
curl http://localhost:3000
# Expected: HTML response (Next.js page)
```

If Phase II isn't working, fix it before proceeding.

---

## 2. Environment Setup

### 2.1 Clone Repository (if not already done)
```bash
git clone <repository-url>
cd todo_app_hct
```

### 2.2 Backend Environment Variables
Create or update `backend/.env`:

```bash
# Existing Phase II variables
DATABASE_URL=postgresql://user:pass@host/dbname  # Neon PostgreSQL
BETTER_AUTH_SECRET=<your-32-char-secret>
CORS_ORIGINS=http://localhost:3000

# NEW: Phase III variables
OPENAI_API_KEY=<your-openai-api-key>  # Get from https://platform.openai.com/api-keys
MCP_TOOLS_LOG_LEVEL=INFO              # DEBUG for verbose logging
CHAT_ENDPOINT_TIMEOUT=120             # Seconds (default: 120s)
```

**Get OpenAI API Key**:
1. Visit https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to `.env` file

### 2.3 Frontend Environment Variables
Create or update `frontend/.env.local`:

```bash
# Existing Phase II variables
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=http://localhost:3000

# No new Phase III variables needed for frontend
```

---

## 3. Database Migration

### 3.1 Generate Migration
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Generate migration for conversation tables
alembic revision --autogenerate -m "Add Phase III conversation tables"
```

Expected output:
```
INFO  [alembic.runtime.migration] ... running autogenerate
Generating ... alembic/versions/003_add_phase_iii_conversation_tables.py ... done
```

### 3.2 Review Migration
Open the generated file:
```bash
# Example: alembic/versions/003_add_phase_iii_conversation_tables.py
cat alembic/versions/003_*.py
```

Verify it includes:
- `conversations` table creation
- `messages` table creation
- Indexes on `(user_id, created_at)` and `(conversation_id, created_at)`
- Trigger for updating `conversation.updated_at`

### 3.3 Apply Migration
```bash
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade 002_... -> 003_..., Add Phase III conversation tables
```

### 3.4 Verify Tables
```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Expected output:
# conversations
# messages
# tasks
# users
```

---

## 4. Backend Setup

### 4.1 Install Dependencies
```bash
cd backend

# Install new Phase III dependencies
pip install openai==1.12.0           # OpenAI Agents SDK
pip install mcp-sdk==0.3.0           # MCP SDK
pip install pydantic-settings==2.1.0 # Enhanced config management

# Update requirements.txt
pip freeze > requirements.txt
```

### 4.2 Verify Installation
```python
# Test OpenAI SDK
python -c "import openai; print(openai.__version__)"
# Expected: 1.12.0

# Test MCP SDK
python -c "import mcp; print('MCP SDK installed')"
# Expected: MCP SDK installed
```

### 4.3 Project Structure Check
Verify Phase III directories exist:
```bash
ls -la src/
# Expected new directories:
# agents/      (subagent implementations)
# mcp/         (MCP tool wrappers)
# routes/chat.py (chat endpoint - may not exist yet)
# models/conversation.py (may not exist yet)
```

If missing, create them:
```bash
mkdir -p src/agents src/mcp
touch src/agents/__init__.py
touch src/mcp/__init__.py
```

### 4.4 Start Backend
```bash
uvicorn src.main:app --reload --port 8000
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 5. Frontend Setup

### 5.1 Install Dependencies
```bash
cd frontend

# Install OpenAI ChatKit
npm install @openai/chatkit@latest

# Install additional UI dependencies
npm install date-fns  # For timestamp formatting
```

### 5.2 Verify Installation
```bash
npm list @openai/chatkit
# Expected: @openai/chatkit@<version>
```

### 5.3 Start Frontend
```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  - ready in 2.5s
```

---

## 6. Testing the Integration

### 6.1 Authenticate First
Before testing chat, you need an auth token:

```bash
# Method 1: Use existing Better Auth login
# 1. Open http://localhost:3000 in browser
# 2. Log in with your credentials
# 3. Open browser DevTools > Application > Local Storage
# 4. Find and copy the JWT token

# Method 2: Create test user via API (if signup enabled)
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

Save the token:
```bash
export JWT_TOKEN="<your-jwt-token-here>"
```

### 6.2 Test Chat Endpoint
Create your first conversation:

```bash
# Test 1: Create task via chat
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "✓ Created task: 'Buy groceries' (ID: 42). I've added it to your list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "title": "Buy groceries"
      },
      "result": {
        "success": true,
        "task_id": 42
      }
    }
  ]
}
```

### 6.3 Test Conversation Continuity
Use the conversation_id from above:

```bash
# Test 2: Continue conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Show me all my tasks"
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Here are your tasks:\n1. Buy groceries (pending)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "parameters": {
        "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "status": "all"
      },
      "result": {
        "success": true,
        "tasks": [{"id": 42, "title": "Buy groceries", "completed": false}]
      }
    }
  ]
}
```

### 6.4 Test Frontend Chat UI
1. Open http://localhost:3000/chat in browser
2. Type: "Add a task to call mom"
3. Click Send
4. Verify response appears in chat window

---

## 7. Development Workflow

### 7.1 Backend Development Loop
```bash
# 1. Make code changes
vim src/agents/intent_classifier.py

# 2. Auto-reload via uvicorn (already running with --reload)

# 3. Test changes
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "test message"}'

# 4. Check logs
tail -f backend/logs/mcp_tools.log
```

### 7.2 Frontend Development Loop
```bash
# 1. Make UI changes
vim src/components/chat/ChatInterface.tsx

# 2. Hot-reload automatic via Next.js

# 3. Test in browser
# Open http://localhost:3000/chat
```

### 7.3 Database Inspection
```bash
# Connect to DB
psql $DATABASE_URL

# View conversations
SELECT * FROM conversations ORDER BY updated_at DESC LIMIT 5;

# View messages
SELECT role, content, created_at
FROM messages
WHERE conversation_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY created_at ASC;

# View tasks
SELECT * FROM tasks WHERE user_id = '<your-user-id>' ORDER BY created_at DESC;
```

### 7.4 Running Tests
```bash
# Backend unit tests
cd backend
pytest tests/test_mcp_tools.py -v

# Backend integration tests
pytest tests/test_conversation_flow.py -v

# Frontend tests
cd frontend
npm test

# E2E tests (requires both servers running)
npm run test:e2e
```

---

## 8. Troubleshooting

### Issue: "OpenAI API key not found"
**Symptom**: Chat endpoint returns 500 error
**Solution**:
```bash
# Verify .env file
cat backend/.env | grep OPENAI_API_KEY

# Restart backend
# Ctrl+C to stop
uvicorn src.main:app --reload --port 8000
```

### Issue: "Conversation not found"
**Symptom**: 404 error when continuing conversation
**Solution**:
```bash
# Check if conversation exists
psql $DATABASE_URL -c "SELECT * FROM conversations WHERE id = '<conversation-id>';"

# If not found, create new conversation (omit conversation_id in request)
```

### Issue: "Database connection refused"
**Symptom**: Backend startup fails
**Solution**:
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Verify Neon database is running (check Neon dashboard)
```

### Issue: "CORS error in browser"
**Symptom**: Frontend can't reach backend
**Solution**:
```bash
# Update backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Restart backend
```

### Issue: "ChatKit not rendering"
**Symptom**: Blank chat page
**Solution**:
```bash
# Check browser console for errors
# Verify ChatKit import:
cat frontend/src/app/chat/page.tsx | grep "ChatKit"

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Next Steps

1. **Read the Architecture**: Review `specs/003-ai-chatbot/plan.md`
2. **Implement Subagents**: Start with `IntentClassifierAgent`
3. **Add Tests**: Write unit tests for each MCP tool
4. **Customize UI**: Style ChatKit to match your brand
5. **Deploy**: Follow Phase IV deployment guide (Kubernetes)

---

## Useful Commands Reference

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
pytest -v
alembic upgrade head

# Frontend
cd frontend
npm run dev
npm test
npm run build

# Database
psql $DATABASE_URL
alembic current
alembic history

# Logs
tail -f backend/logs/mcp_tools.log
tail -f backend/logs/uvicorn.log
```

---

## Resources

- [OpenAI Agents SDK Docs](https://platform.openai.com/docs/agents)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI ChatKit](https://github.com/openai/chatkit)
- [Phase III Specification](./spec.md)
- [Phase III Architecture Plan](./plan.md)

---

**Questions?** Check the troubleshooting section or review the full documentation in `specs/003-ai-chatbot/`.

**Ready to implement?** Proceed to `/sp.tasks` to generate the task breakdown!
