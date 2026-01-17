# Feature Specification: Phase III – Todo AI Chatbot

**Phase**: Phase III - AI Conversational Layer
**Created**: 2026-01-13
**Status**: Draft
**Foundation**: Built on Phase II (Full-Stack Web + Auth)

## 1. Objective

Create an AI-powered conversational chatbot that allows authenticated users to manage todo tasks using natural language. The system must use a **stateless architecture**, OpenAI Agents SDK for AI logic, and MCP (Model Context Protocol) tools for task operations.

The chatbot translates user intent into deterministic MCP tool calls while persisting conversation state in the database.

## Clarifications

### Session 2026-01-14

- Q: What is the acceptable response time for the chat endpoint (p95 latency)? → A: < 5 seconds (balanced for AI processing)
- Q: When the OpenAI API fails or times out, what should the chat endpoint do? → A: Retry once with fixed 500ms delay
- Q: What rate limiting should be applied to the chat endpoint? → A: 100 requests per hour per user
- Q: When a conversation is deleted, what should happen to its messages? → A: Soft delete (set deleted_at) with optional asynchronous archival
- Q: What observability should be implemented for production monitoring? → A: Structured logging with correlation IDs

## 2. Scope

### 2.1 In Scope
- Conversational interface for all basic task operations
- Stateless chat API endpoint
- MCP server exposing task operations as tools
- Conversation persistence in database
- Agent-driven tool orchestration

### 2.2 Out of Scope
- Voice commands
- Multi-language support
- Notifications or reminders
- Refactoring Phase I or Phase II logic

## 3. Technology Stack

| Component | Technology |
|--------|-----------|
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth |

## 4. Architecture

```
ChatKit UI
|
v
POST /api/{user_id}/chat
|
v
FastAPI Server
|
v
OpenAI Agents SDK (Agent + Runner)
|
v
MCP Server (Task Tools)
|
v
Neon PostgreSQL
```

### Architectural Constraints
- Server must be stateless
- Database is the single source of truth
- Agents must not access the database directly
- All task operations must be performed via MCP tools

## 5. Database Models

### 5.1 Task

| Field | Description |
|----|-----------|
| id | Task ID |
| user_id | Task owner |
| title | Task title |
| description | Optional description |
| completed | Completion status |
| created_at | Creation timestamp |
| updated_at | Update timestamp |

### 5.2 Conversation

| Field | Description |
|----|-----------|
| id | Conversation ID |
| user_id | Owner |
| created_at | Creation timestamp |
| updated_at | Update timestamp |
| deleted_at | Soft delete timestamp (NULL if active) |

### 5.3 Message

| Field | Description |
|----|-----------|
| id | Message ID |
| user_id | Owner |
| conversation_id | Parent conversation |
| role | user / assistant |
| content | Message text |
| created_at | Timestamp |
| deleted_at | Soft delete timestamp (NULL if active) |

Messages must be append-only.

### 5.4 Deletion Strategy

When a conversation is deleted:
1. Set `deleted_at` timestamp on the conversation record
2. Set `deleted_at` timestamp on all associated messages
3. Exclude soft-deleted records from all user-facing queries
4. An asynchronous archival job MAY copy soft-deleted conversations and messages to `archived_conversations` and `archived_messages` after a defined retention period
5. Archived data is retained for audit and recovery purposes

## 6. Chat API Endpoint

### Endpoint
`POST /api/{user_id}/chat`

### Request Body

| Field | Required | Description |
|----|--------|-------------|
| conversation_id | No | Existing conversation ID |
| message | Yes | User natural language message |

### Response Body

| Field | Description |
|----|-------------|
| conversation_id | Conversation ID |
| response | AI assistant response |
| tool_calls | MCP tools invoked |

## 7. MCP Tools Specification

### add_task

**Purpose:** Create a new task

**Parameters**
```json
{
  "user_id": "string",
  "title": "string",
  "description": "string (optional)"
}
```

**Returns**
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### list_tasks

**Purpose:** Retrieve tasks

**Parameters**
```json
{
  "user_id": "string",
  "status": "all | pending | completed (optional)"
}
```

**Returns**
```json
[
  { "id": 1, "title": "Buy groceries", "completed": false }
]
```

### complete_task

**Purpose:** Mark task as completed

**Parameters**
```json
{
  "user_id": "string",
  "task_id": "integer"
}
```

**Returns**
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

### delete_task

**Purpose:** Delete a task

**Parameters**
```json
{
  "user_id": "string",
  "task_id": "integer"
}
```

**Returns**
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

### update_task

**Purpose:** Update task title and/or description

**Parameters**
```json
{
  "user_id": "string",
  "task_id": "integer",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Returns**
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

## 8. Agent Behavior Specification

### Intent Mapping

| User Intent | MCP Tool |
|------------|----------|
| Add / create / remember | add_task |
| Show / list | list_tasks |
| Done / complete | complete_task |
| Delete / remove | delete_task |
| Change / update | update_task |

### Rules
- Agent must always confirm actions
- Agent must never guess task IDs
- Ambiguous references require list_tasks before action
- Errors must be handled gracefully

## 9. Stateless Conversation Flow

1. Receive user message
2. Fetch conversation history from database
3. Build agent input (history + new message)
4. Store user message
5. Run agent with MCP tools
6. Agent invokes MCP tool(s)
7. Store assistant response
8. Return response to client

Server retains no state.

## 10. Natural Language Examples

| User Input | Expected Behavior |
|-----------|------------------|
| Add a task to buy groceries | add_task |
| Show me all my tasks | list_tasks (all) |
| What's pending? | list_tasks (pending) |
| Mark task 3 as complete | complete_task |
| Delete the meeting task | list_tasks → delete_task |
| Change task 1 to call mom | update_task |
| What have I completed? | list_tasks (completed) |

## 11. Deliverables

- /frontend – ChatKit UI
- /backend – FastAPI + Agents SDK + MCP
- /specs – Specification files
- Database migration scripts
- README with setup instructions

## 12. Non-Functional Requirements

### Performance
- Chat endpoint p95 latency: < 5 seconds (includes OpenAI API processing time)
- MCP tool call latency: < 100ms p95
- Database query latency: < 50ms p95

### Architecture & Reliability
- Stateless architecture
- Deterministic behavior
- Idempotent tool calls
- Horizontal scalability
- Graceful error handling

### Error Handling & Resilience
- OpenAI API failures: Retry once with fixed 500ms delay before returning error
- MCP tool failures: Retry once with 500ms delay
- Database connection errors: Surface user-friendly error message
- All errors must return structured error responses with appropriate HTTP status codes

### Security & Rate Limiting
- Rate limiting: 100 requests per hour per authenticated user
- All MCP tools must enforce user_id isolation (no cross-user data access)
- JWT token validation required for all chat endpoints
- Input sanitization on all user messages before processing

### Observability
- Structured logging with correlation IDs for request tracing
- Log all chat endpoint requests with: user_id, conversation_id, timestamp, latency
- Log all MCP tool invocations with: tool_name, parameters, result, latency
- Log all errors with stack traces and context
- Correlation IDs propagate through: API → Agent → MCP Tools → Database
- Log levels: INFO (requests/responses), WARN (retries), ERROR (failures)
