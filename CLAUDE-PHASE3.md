# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# Phase III: AI Chatbot Interface

**Current Phase**: Phase III - AI Conversational Layer
**Foundation**: Built on Phase II (Full-Stack Web + Auth)
**Architecture**: Stateless, MCP-based, Subagent-driven

---

## 🚨 ABSOLUTE HARD CONSTRAINT — PHASE II IS FROZEN (READ THIS FIRST)

### ✅ Allowed Work (EXHAUSTIVE LIST)

Claude is authorized to work **ONLY** on the following:

1. **AI Chatbot Logic**
   - IntentClassifierAgent, TaskResolutionAgent, ActionAgent, ResponseFormatterAgent
   - Agent orchestration in `backend/src/services/chatbot_service.py`
   - OpenAI Agents SDK integration

2. **MCP Server**
   - Official MCP SDK implementation
   - MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
   - MCP tool wrappers in `backend/src/mcp/task_tools.py`
   - MCP logging infrastructure

3. **Chat API Endpoints (NEW ONLY)**
   - `POST /api/chat` - Chat endpoint
   - `GET /api/conversations` - List conversations
   - `GET /api/conversations/{id}/messages` - Get messages
   - Chat request/response schemas

4. **Database Models (CHAT ONLY)**
   - `Conversation` model in `backend/src/models/conversation.py`
   - `Message` model in `backend/src/models/conversation.py`
   - Alembic migration for conversation/message tables

5. **Frontend Chat UI (NEW ONLY)**
   - OpenAI ChatKit integration
   - `frontend/src/components/chat/` directory (NEW components only)
   - `frontend/src/app/chat/` route (NEW page only)
   - Chat-specific services in `frontend/src/services/chat_service.ts`

6. **Phase III Specs**
   - `specs/003-ai-chatbot/` directory only
   - Planning documents (spec.md, plan.md, tasks.md, research.md, etc.)

7. **Backend Logic (ADDITIVE ONLY)**
   - New files in `backend/src/agents/`
   - New files in `backend/src/mcp/`
   - New routes in `backend/src/routes/chat.py`, `backend/src/routes/conversations.py`
   - Does NOT modify Phase II behavior

### ⛔ STRICT PROHIBITION (PHASE II IS READ-ONLY)

Claude **MUST NOT** under **ANY** circumstances:

#### ❌ Frontend (Phase II Frozen)
- ❌ Modify Phase II UI components
- ❌ Modify Phase II UX flows
- ❌ Modify Phase II styling (CSS, Tailwind)
- ❌ Modify `tailwind.config.ts`
- ❌ Modify shadcn/ui components
- ❌ Modify frontend layouts (`frontend/src/app/layout.tsx`)
- ❌ Modify existing pages (`frontend/src/app/page.tsx`, `frontend/src/app/tasks/`, etc.)
- ❌ Modify existing components (`frontend/src/components/` except `/chat/`)
- ❌ Modify icons, themes, or design tokens
- ❌ Refactor existing frontend code
- ❌ Rename frontend components
- ❌ Change routing structure (except adding `/chat` route)

#### ❌ Backend (Phase II Frozen)
- ❌ Change API contracts defined in Phase II
- ❌ Modify existing REST endpoints (`/api/tasks`, `/api/auth`, etc.)
- ❌ Change authentication behavior (Better Auth configuration)
- ❌ Modify database schema for `tasks` or `users` tables
- ❌ Modify existing models (`backend/src/models/task.py`, `backend/src/models/user.py`)
- ❌ Modify existing services (`backend/src/services/task_service.py`)
- ❌ Modify existing routes (`backend/src/routes/tasks.py`, `backend/src/routes/auth.py`)
- ❌ Change CORS configuration (except adding `/api/chat` to allowed origins)
- ❌ Modify Alembic migrations from Phase I/II

#### ❌ Configuration (Phase II Frozen)
- ❌ Modify `frontend/package.json` dependencies (except adding OpenAI ChatKit)
- ❌ Modify `backend/requirements.txt` dependencies (except adding OpenAI SDK, MCP SDK)
- ❌ Change environment variable names from Phase II
- ❌ Modify `.env.example` entries from Phase II (can only ADD new Phase III vars)

### 🔒 Phase II is READ-ONLY

**Phase II frontend and backend functionality is LOCKED.**

Claude may:
- ✅ **Read** Phase II code for reference
- ✅ **Call** Phase II API endpoints from new chat UI
- ✅ **Reuse** Phase II authentication (JWT extraction)
- ✅ **Reference** Phase II database models (Task, User)

Claude **MUST NOT**:
- ❌ **Modify** any Phase II files
- ❌ **Optimize** Phase II code
- ❌ **Refactor** Phase II structure
- ❌ **"Improve"** Phase II UX/UI

**No exceptions. No optimizations. No "minor improvements".**

### ⚠️ IF UNSURE — STOP IMMEDIATELY

If Claude is uncertain whether a change:
- Touches Phase II UI/UX
- Alters Phase II behavior
- Breaks existing functionality
- Modifies Phase II files

👉 **Claude MUST STOP and ASK, not guess.**

### 💀 FAILURE CONDITIONS (AUTO-DISQUALIFY)

Claude is considered **FAILED** if it:
1. ❌ Modifies Phase II UI/UX (instant disqualification)
2. ❌ Breaks existing Phase II functionality
3. ❌ Introduces hidden state (violates stateless architecture)
4. ❌ Bypasses MCP (agents access database directly)
5. ❌ Changes Phase II API contracts
6. ❌ Alters authentication flow
7. ❌ Modifies Phase I/II database schema

**Violation of any above = Immediate failure. No recovery.**

---

## Critical Phase III Rules

### Authority & Source of Truth

1. **Spec-First Development** (NON-NEGOTIABLE)
   - All Phase III features MUST have specifications in `specs/003-ai-chatbot/`
   - Reference `.specify/memory/constitution.md` for governance
   - CLAUDE.md defines rules, boundaries, and workflow instructions
   - Existing Phase I/II code is **reference only** - DO NOT modify unless spec explicitly allows

2. **Phase Discipline**
   - Phase III adds **conversational AI layer ONLY**
   - Core task CRUD logic from Phase I & II **MUST NOT be modified**
   - All changes are **additive only** - no core logic deletion or replacement

3. **Agent Boundaries** (CRITICAL)
   - Agents **CANNOT access database directly**
   - Agents **CANNOT infer user identity** (must extract from JWT)
   - All operations that modify or fetch tasks **MUST go through MCP tools ONLY**
   - Agents **MUST NOT store state in memory** - conversation context is fetched from and stored to DB
   - Agents **MUST confirm actions** if ambiguity exists

### Stateless Architecture

```
User → Frontend ChatKit → Backend Chatbot API → Subagents → MCP Tools → Database
                                                        ↓
                                                 Conversation stored in DB
                                                 (single source of truth)
```

**Key Principle**: Server holds **NO state** between requests. Database is single source of truth for both tasks AND conversation history.

## Subagent Architecture

Phase III uses a **multi-agent system** with strict separation of concerns:

### 1. IntentClassifierAgent
- **Purpose**: Parse user message → `{intent, confidence, entities}`
- **Input**: Raw user message (string)
- **Output**: `{intent: string, confidence: float, entities: dict}`
- **Rules**:
  - Confidence threshold enforced (e.g., >0.7 for execution, <0.7 request clarification)
  - Pure classification - **NO tool calls allowed**
  - Intents: `create_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`, `unclear`
- **Example**:
  ```
  Input: "remind me to call mom tomorrow"
  Output: {intent: "create_task", confidence: 0.92, entities: {title: "call mom", due_date: "tomorrow"}}
  ```

### 2. TaskResolutionAgent
- **Purpose**: Resolve ambiguous task references (e.g., "the first one", "my task about groceries")
- **Input**: `{entities: dict, user_id: str}`
- **Output**: `{task_ids: [int], confirmation_needed: bool}`
- **Allowed operations**: `list_tasks` MCP tool ONLY (read-only)
- **Rules**:
  - Always confirm if multiple matches exist - **DO NOT choose arbitrarily**
  - Use semantic matching for fuzzy search (e.g., "groceries" matches "buy groceries")
  - Return empty list if no match found
- **Example**:
  ```
  Input: {entities: {reference: "my task about groceries"}, user_id: "user-123"}
  Tool Call: list_tasks(user_id="user-123")
  Output: {task_ids: [5, 12], confirmation_needed: true} → "Did you mean 'Buy groceries' or 'Grocery shopping list'?"
  ```

### 3. ActionAgent
- **Purpose**: Map intent → MCP tool execution
- **Input**: `{intent: string, parameters: dict, user_id: str}`
- **Output**: MCP tool execution result (success/error)
- **Allowed operations**: `add_task`, `update_task`, `complete_task`, `delete_task`, `list_tasks` (via MCP)
- **Rules**:
  - Parameters MUST be validated before execution
  - Execution MUST be idempotent (safe to retry)
  - **NEVER bypass MCP tools** to access database directly
  - Extract user_id from JWT, pass to MCP tools for isolation
- **Example**:
  ```
  Input: {intent: "create_task", parameters: {title: "call mom", due_date: "2026-01-14"}, user_id: "user-123"}
  Tool Call: add_task(user_id="user-123", title="call mom", due_date="2026-01-14")
  Output: {success: true, task: {...}}
  ```

### 4. ResponseFormatterAgent
- **Purpose**: Convert MCP tool output → user-friendly natural language response
- **Input**: MCP tool output (JSON)
- **Output**: Text response to user (string)
- **Rules**:
  - Confirm success/failure clearly
  - Format data for readability (e.g., list tasks as bullet points)
  - NO additional logic - pure formatting only
  - Be concise and conversational
- **Example**:
  ```
  Input: {success: true, task: {id: 42, title: "call mom", completed: false}}
  Output: "✓ Created task: 'call mom' (ID: 42). I've added it to your list!"
  ```

## Conversation Flow (Stateless)

```
1. User sends message → Frontend ChatKit component

2. Frontend → Backend POST /api/chat
   - JWT token in Authorization header (extract user_id)
   - Message body: {message: "remind me to call mom", conversation_id: "conv-123"}

3. Backend preprocessing:
   - Normalize text (lowercase, trim)
   - Load conversation context from DB (conversation_id + user_id)

4. IntentClassifierAgent:
   - Classify intent + extract entities
   - Return: {intent, confidence, entities}

5. TaskResolutionAgent (if needed):
   - Resolve task references (e.g., "the first one" → task_id: 5)
   - Confirm if ambiguous

6. ActionAgent:
   - Execute MCP tool based on intent
   - Pass user_id for isolation
   - Return tool result

7. ResponseFormatterAgent:
   - Format tool output → natural language
   - Return response text

8. Backend persistence:
   - Append user message to DB (conversation_id, user_id, role: "user", content: message)
   - Append agent response to DB (conversation_id, user_id, role: "assistant", content: response)

9. Frontend:
   - Display response in ChatKit
   - Update UI state
```

## MCP Tools (Phase III)

All task operations **MUST** go through MCP tools. Direct database access is **PROHIBITED**.

### Available MCP Tools

1. **add_task**
   ```python
   def add_task(user_id: str, title: str, description: str = "", due_date: str = None, priority: str = "medium") -> dict:
       """Create new task for user. Returns {success: bool, task: dict}"""
   ```

2. **list_tasks**
   ```python
   def list_tasks(user_id: str, status: str = "all", limit: int = 50) -> dict:
       """Get tasks for user. Status: 'all' | 'pending' | 'completed'. Returns {success: bool, tasks: [dict]}"""
   ```

3. **update_task**
   ```python
   def update_task(user_id: str, task_id: int, **kwargs) -> dict:
       """Update task fields. Returns {success: bool, task: dict}"""
   ```

4. **complete_task**
   ```python
   def complete_task(user_id: str, task_id: int, completed: bool = True) -> dict:
       """Toggle task completion. Returns {success: bool, task: dict}"""
   ```

5. **delete_task**
   ```python
   def delete_task(user_id: str, task_id: int) -> dict:
       """Soft-delete task (sets deleted_at). Returns {success: bool}"""
   ```

### MCP Tool Rules

- **User Isolation**: Every tool MUST filter by user_id (extracted from JWT)
- **Validation**: Tools validate parameters before DB operations
- **Error Handling**: Return `{success: false, error: "message"}` on failure
- **Idempotency**: Safe to call multiple times (e.g., completing completed task is no-op)

## Semantic Understanding

Phase III supports natural language task references:

### Fuzzy Matching Examples

```
User: "mark the grocery one as done"
  ↓ TaskResolutionAgent
  → list_tasks(user_id) → find task with title containing "grocery"
  → task_id: 5 ("Buy groceries")
  ↓ ActionAgent
  → complete_task(user_id, task_id=5)
```

```
User: "delete my second task"
  ↓ TaskResolutionAgent
  → list_tasks(user_id) → get all tasks, select index 1 (0-indexed)
  → task_id: 12
  ↓ Confirm: "Delete 'Call dentist'? (Y/N)"
```

### Low Confidence Handling

If IntentClassifierAgent returns confidence < 0.7:

```
User: "do the thing with tasks"
  ↓ IntentClassifierAgent
  → {intent: "unclear", confidence: 0.45}
  ↓ ResponseFormatterAgent
  → "I'm not sure what you want to do. Can you rephrase? Try: 'show my tasks' or 'create a new task'"
```

## Failure Handling

### Task Not Found
```
User: "complete task 999"
  ↓ ActionAgent → complete_task(user_id, task_id=999)
  → {success: false, error: "Task not found"}
  ↓ ResponseFormatterAgent
  → "I couldn't find task #999. Try 'show my tasks' to see your task list."
```

### Ambiguous Reference
```
User: "update the first one"
  ↓ TaskResolutionAgent → list_tasks(user_id)
  → Multiple tasks found
  ↓ ResponseFormatterAgent
  → "You have multiple tasks. Which one? 1) Buy groceries 2) Call dentist"
```

### Invalid Parameters
```
User: "create task with title ''"
  ↓ ActionAgent → add_task(user_id, title="")
  → {success: false, error: "Title cannot be empty"}
  ↓ ResponseFormatterAgent
  → "Task title is required. Please provide a task name."
```

### Database Connection Error
```
ActionAgent → MCP tool → Database error
  ↓
Retry: 1 attempt with 500ms delay
  ↓
If still fails:
  → {success: false, error: "Service temporarily unavailable"}
  ↓ ResponseFormatterAgent
  → "I'm having trouble connecting to the database. Please try again in a moment."
```

## Logging & Auditing (REQUIRED)

Every MCP tool call MUST log:

```json
{
  "timestamp": "2026-01-13T10:30:00Z",
  "user_id": "user-123",
  "conversation_id": "conv-456",
  "tool": "add_task",
  "parameters": {"title": "call mom", "due_date": "2026-01-14"},
  "result": {"success": true, "task_id": 42},
  "latency_ms": 87
}
```

**Log Storage**: Append-only logs in `backend/logs/mcp_tools.log`
**Purpose**: Audit trail, debugging, future event-driven integrations (Phase IV: Kafka)

## Development Commands

### Backend (FastAPI)

```bash
cd backend

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure DATABASE_URL, BETTER_AUTH_SECRET

# Run
uvicorn src.main:app --reload --port 8000

# Test
pytest                           # Run all tests
pytest tests/test_mcp_tools.py  # Test MCP tools
pytest tests/test_chatbot.py    # Test chatbot API
pytest -v -s                    # Verbose with stdout

# Database
alembic revision --autogenerate -m "Add conversation table"
alembic upgrade head
```

### Frontend (Next.js)

```bash
cd frontend

# Setup
npm install
cp .env.local.example .env.local  # Configure NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET

# Run
npm run dev  # Starts on port 3000 (or 3001-3005 if occupied)

# Build
npm run build  # Production build (SSR required)
npm start      # Serve production build

# Test
npm test       # Run Jest tests
npm run lint   # ESLint + TypeScript checks
```

### Phase III Specific

```bash
# Test MCP tools in isolation
cd backend
python -m pytest tests/test_mcp_tools.py -v

# Test subagents
python -m pytest tests/test_intent_classifier.py -v
python -m pytest tests/test_task_resolution.py -v
python -m pytest tests/test_action_agent.py -v
python -m pytest tests/test_response_formatter.py -v

# Test full conversation flow
python -m pytest tests/test_conversation_flow.py -v

# Run chatbot API manually
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "show my tasks", "conversation_id": "test-conv"}'
```

## Project Structure (Phase III Additions)

```
todo_app_hct/
├── backend/
│   ├── src/
│   │   ├── agents/                    # NEW: Subagent implementations
│   │   │   ├── __init__.py
│   │   │   ├── intent_classifier.py   # IntentClassifierAgent
│   │   │   ├── task_resolution.py     # TaskResolutionAgent
│   │   │   ├── action_agent.py        # ActionAgent
│   │   │   └── response_formatter.py  # ResponseFormatterAgent
│   │   ├── mcp/                       # NEW: MCP tool wrappers
│   │   │   ├── __init__.py
│   │   │   └── task_tools.py          # add_task, list_tasks, etc.
│   │   ├── routes/
│   │   │   ├── chat.py                # NEW: POST /api/chat endpoint
│   │   │   └── conversations.py       # NEW: Conversation CRUD
│   │   ├── models/
│   │   │   ├── conversation.py        # NEW: Conversation & Message models
│   │   │   └── task.py                # Existing (DO NOT MODIFY)
│   │   └── services/
│   │       └── chatbot_service.py     # NEW: Orchestrates subagents
│   └── tests/
│       ├── test_mcp_tools.py          # NEW: MCP tool tests
│       ├── test_intent_classifier.py  # NEW: Intent classifier tests
│       └── test_conversation_flow.py  # NEW: End-to-end flow tests
├── frontend/
│   └── src/
│       ├── components/
│       │   └── chat/                  # NEW: ChatKit component
│       │       ├── ChatInterface.tsx
│       │       ├── MessageBubble.tsx
│       │       └── InputBar.tsx
│       └── app/
│           └── chat/                  # NEW: /chat route
│               └── page.tsx
└── specs/
    └── 003-ai-chatbot/                # NEW: Phase III specs
        ├── spec.md                    # Requirements
        ├── plan.md                    # Architecture
        └── tasks.md                   # Task breakdown
```

## Architecture Principles (Phase III)

### 1. Stateless Design
- **NO in-memory state** between requests
- Conversation context loaded from DB on every request
- Database is single source of truth

### 2. MCP-Only Access
- **NO direct database queries** in agent code
- All CRUD operations through MCP tools
- MCP tools enforce user isolation

### 3. Subagent Autonomy
- Each subagent has **single, well-defined responsibility**
- IntentClassifier: Parse only (no tool calls)
- TaskResolution: Resolve references (list_tasks only)
- ActionAgent: Execute tools (all CRUD tools)
- ResponseFormatter: Format only (no logic)

### 4. Confirmation over Assumption
- **Always confirm** if ambiguity exists
- Low confidence → ask user for clarification
- Multiple matches → present options, let user choose
- **NEVER guess** user intent or task IDs

### 5. Additive Changes Only
- Phase I/II code is **off-limits**
- New files ONLY (no modifications to existing core logic)
- Extend functionality, don't replace

## Do's and Don'ts

### ✅ Do's

- Follow specs in `specs/003-ai-chatbot/` strictly
- Use MCP tools for ALL task operations
- Confirm user actions if ambiguity exists
- Fetch conversation context from DB on every request
- Return clear, concise natural language responses
- Handle errors gracefully with user-friendly messages
- Log all MCP tool calls for audit trail
- Test each subagent independently before integration

### ❌ Don'ts

- ❌ Store conversation or task state in memory
- ❌ Infer user identity (extract from JWT only)
- ❌ Bypass MCP tools to access database directly
- ❌ Modify Phase I/II core logic (task models, CRUD services)
- ❌ Hallucinate data or invent task details
- ❌ Choose arbitrarily between multiple matches (always confirm)
- ❌ Use synchronous blocking calls (async/await for all I/O)
- ❌ Fail silently (always return error messages to user)

## SDD Workflow for Phase III

All Phase III development follows Spec-Driven Development:

1. **Spec Creation**: `specs/003-ai-chatbot/spec.md` (requirements, user stories, acceptance criteria)
2. **Planning**: `specs/003-ai-chatbot/plan.md` (architecture, subagent design, MCP tools)
3. **Task Breakdown**: `specs/003-ai-chatbot/tasks.md` (testable tasks with TDD cases)
4. **Implementation**: Build subagents, MCP tools, chatbot API
5. **Testing**: Unit tests (each subagent), integration tests (conversation flow), E2E tests
6. **Validation**: SpecAgent validates compliance, TestAgent runs test suite
7. **Documentation**: Update PHRs, create ADRs for significant decisions

## Environment Variables (Phase III)

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host/dbname  # Neon PostgreSQL
BETTER_AUTH_SECRET=<32-char-secret>              # JWT signing key
CORS_ORIGINS=http://localhost:3000               # Frontend origin
OPENAI_API_KEY=<your-openai-key>                 # NEW: For LLM agents
MCP_TOOLS_LOG_LEVEL=INFO                         # NEW: MCP tool logging

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000        # Backend URL
BETTER_AUTH_SECRET=<same-as-backend>             # JWT validation
BETTER_AUTH_URL=http://localhost:3000            # Frontend URL
```

## Testing Strategy (Phase III)

### Unit Tests (Per Subagent)

```python
# tests/test_intent_classifier.py
def test_create_task_intent():
    agent = IntentClassifierAgent()
    result = agent.classify("remind me to call mom")
    assert result["intent"] == "create_task"
    assert result["confidence"] > 0.7
    assert "call mom" in result["entities"]["title"]
```

### Integration Tests (Conversation Flow)

```python
# tests/test_conversation_flow.py
def test_full_conversation_flow(client, auth_headers):
    # User creates task via chat
    response = client.post("/api/chat",
        json={"message": "add task: buy milk"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Created task" in response.json()["response"]

    # User lists tasks via chat
    response = client.post("/api/chat",
        json={"message": "show my tasks"},
        headers=auth_headers
    )
    assert "buy milk" in response.json()["response"]
```

### E2E Tests (Frontend + Backend)

```typescript
// tests/e2e/chat.spec.ts
test('user can create task via chat', async ({ page }) => {
  await page.goto('/chat');
  await page.fill('[data-testid="chat-input"]', 'remind me to call dentist');
  await page.click('[data-testid="chat-send"]');
  await expect(page.locator('[data-testid="chat-message"]').last()).toContainText('Created task');
});
```

## API Documentation

**Base URL**: `http://localhost:8000`

### Chatbot Endpoints (Phase III)

```
POST /api/chat
  Description: Send message to chatbot, receive response
  Auth: Required (JWT in Authorization header)
  Body: {message: string, conversation_id?: string}
  Response: {response: string, conversation_id: string}

GET /api/conversations
  Description: List user's conversations
  Auth: Required
  Response: {conversations: [{id, created_at, updated_at, message_count}]}

GET /api/conversations/{id}/messages
  Description: Get conversation messages
  Auth: Required
  Response: {messages: [{role, content, timestamp}]}
```

**Swagger UI**: http://localhost:8000/docs (when backend running)

## Constitution Reference

See `.specify/memory/constitution.md` for:
- Agent governance and scopes
- Workflow governance (SDD pipeline)
- Deployment governance
- Compliance and escalation rules

**Key Agents for Phase III**:
- **ChatbotAgent**: Natural language interpretation, LLM integration, conversational UI
- **TaskCRUDAgent**: Task CRUD operations (via MCP tools)
- **AuthenticationAgent**: JWT validation (existing from Phase II)

## Common Pitfalls to Avoid

1. **Direct Database Access**: Always use MCP tools, never query DB directly
2. **Stateful Agents**: Don't store conversation state in memory - load from DB
3. **Arbitrary Choices**: Always confirm when multiple matches exist
4. **Modifying Core Logic**: Phase I/II code is off-limits - additive changes only
5. **Missing User Isolation**: All MCP tools must filter by user_id from JWT
6. **Silent Failures**: Always return user-friendly error messages
7. **Synchronous Blocking**: Use async/await for all I/O operations
8. **Hallucinating Data**: Never invent task IDs, titles, or user data

## Phase III Success Criteria

- ✅ Users can interact with tasks via natural language chat
- ✅ Subagents correctly classify intent, resolve references, execute tools, format responses
- ✅ MCP tools enforce user isolation (no cross-user access)
- ✅ Conversation history persists in database (stateless architecture)
- ✅ All task operations map to Phase II backend (no core logic changes)
- ✅ Error handling provides clear feedback to users
- ✅ Logging captures all MCP tool calls for audit trail
- ✅ Integration tests verify end-to-end conversation flows

---

**Remember**: Phase III is about adding conversational intelligence **on top of** existing Phase II infrastructure. Respect phase boundaries, use MCP tools exclusively, and maintain stateless design.
