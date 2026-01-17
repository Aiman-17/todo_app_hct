# Implementation Plan: Phase III – Todo AI Chatbot

**Phase**: Phase III - AI Conversational Layer | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-ai-chatbot/spec.md`

## Summary

Phase III adds a conversational AI layer to the existing todo application, enabling users to manage tasks through natural language. The implementation uses OpenAI Agents SDK for intent classification and response generation, with MCP (Model Context Protocol) tools providing the interface between AI agents and the existing Phase II task CRUD operations. The architecture is stateless - conversation history is persisted in the database, and each request rebuilds context from storage. This phase is additive-only: no modifications to Phase I/II core logic.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Uvicorn
- Frontend: Next.js 16+, React 19+, OpenAI ChatKit, shadcn/ui

**Storage**: Neon Serverless PostgreSQL (existing + new Conversation/Message tables)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web (Linux server + browser)
**Project Type**: Web application (existing backend/frontend structure)
**Performance Goals**:
- Chat endpoint p95 latency: <5 seconds (includes OpenAI API processing time)
- MCP tool call latency: <100ms p95
- Database query latency: <50ms p95
- Support 100 concurrent chat sessions

**Constraints**:
- Stateless architecture (no server-side session storage)
- MCP-only database access (agents cannot query DB directly)
- Additive changes only (no Phase I/II modifications)
- User isolation via JWT (all operations scoped to authenticated user)

**Error Handling & Resilience**:
- OpenAI API failures: Retry once with fixed 500ms delay before returning error
- MCP tool failures: Retry once with 500ms delay
- All errors return structured error responses with appropriate HTTP status codes

**Security & Rate Limiting**:
- Rate limiting: 100 requests per hour per authenticated user
- JWT token validation required for all chat endpoints
- Input sanitization on all user messages before processing

**Observability**:
- Structured logging with correlation IDs for request tracing
- Log all chat endpoint requests with: user_id, conversation_id, timestamp, latency
- Log all MCP tool invocations with: tool_name, parameters, result, latency
- Correlation IDs propagate through: API → Agent → MCP Tools → Database
- Log levels: INFO (requests/responses), WARN (retries), ERROR (failures)

**Scale/Scope**:
- Single-user chat sessions (no multi-user conversations)
- Conversation history up to 1000 messages per conversation
- 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-First Development
- Specification exists at `specs/003-ai-chatbot/spec.md`
- User stories, acceptance criteria, and success metrics defined
- No implementation started before spec approval

### ✅ Agent-Centric Workflow
- ChatbotAgent handles natural language interpretation
- TaskCRUDAgent provides task operations via MCP tools
- AuthenticationAgent validates JWT tokens (existing Phase II)
- TodoMasterAgent coordinates multi-agent workflow

### ✅ Skill Reusability
- MCP tools are versioned, reusable wrappers around existing Phase II CRUD
- Conversation flow is modular (can be extended for future phases)

### ✅ Phase-Based Evolution
- Phase III is additive-only (extends Phase II infrastructure)
- No refactoring of Phase I/II code
- Backward compatible with existing API endpoints

### ✅ Quality & Compliance
- Unit tests required for each MCP tool
- Integration tests for full conversation flow
- SpecAgent will validate compliance before deployment

### ✅ Event-Driven Architecture
- Phase III prepares foundation for Phase IV Kafka integration
- MCP tool logs provide audit trail for future event sourcing
- Async/await pattern throughout for non-blocking I/O

### ✅ Security
- All chat requests require JWT authentication
- User isolation enforced: all MCP tools filter by user_id
- No sensitive data in conversation logs
- Input sanitization for natural language messages

**Constitution Compliance**: ✅ PASS

## Project Structure

### Documentation (Phase III)

```text
specs/003-ai-chatbot/
├── spec.md              # Requirements (completed)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Database schema
├── quickstart.md        # Phase 1: Developer onboarding
├── contracts/           # Phase 1: API contracts
│   ├── chat-api.yaml    # OpenAPI for chat endpoint
│   └── mcp-tools.yaml   # MCP tool specifications
└── tasks.md             # Phase 2: Task breakdown (/sp.tasks command)
```

### Source Code (existing structure extended)

```text
backend/
├── src/
│   ├── agents/                    # NEW: Subagent implementations
│   │   ├── __init__.py
│   │   ├── intent_classifier.py   # IntentClassifierAgent
│   │   ├── task_resolution.py     # TaskResolutionAgent
│   │   ├── action_agent.py        # ActionAgent
│   │   └── response_formatter.py  # ResponseFormatterAgent
│   ├── mcp/                       # NEW: MCP tool wrappers
│   │   ├── __init__.py
│   │   └── task_tools.py          # MCP: add_task, list_tasks, etc.
│   ├── routes/
│   │   ├── chat.py                # NEW: POST /api/chat endpoint
│   │   ├── conversations.py       # NEW: Conversation CRUD
│   │   └── tasks.py               # EXISTING (Phase II)
│   ├── models/
│   │   ├── conversation.py        # NEW: Conversation & Message
│   │   ├── task.py                # EXISTING (DO NOT MODIFY)
│   │   └── user.py                # EXISTING (DO NOT MODIFY)
│   └── services/
│       ├── chatbot_service.py     # NEW: Orchestrates subagents
│       └── task_service.py        # EXISTING (Phase II)
└── tests/
    ├── test_mcp_tools.py          # NEW: MCP tool tests
    ├── test_intent_classifier.py  # NEW: Intent tests
    └── test_conversation_flow.py  # NEW: E2E flow tests

frontend/
├── src/
│   ├── components/
│   │   └── chat/                  # NEW: ChatKit components
│   │       ├── ChatInterface.tsx
│   │       ├── MessageBubble.tsx
│   │       └── InputBar.tsx
│   └── app/
│       └── chat/                  # NEW: /chat route
│           └── page.tsx
└── tests/
    └── chat.spec.ts               # NEW: E2E chat tests
```

**Structure Decision**: Extends existing web application structure (backend/frontend). Phase III adds new directories (`agents/`, `mcp/`, `chat/`) without modifying existing Phase I/II code. This follows the constitution's additive-only principle.

## Complexity Tracking

> **Constitution Check violations: NONE**

No complexity violations. Phase III follows all constitutional principles:
- Spec-first development completed
- Agent-centric workflow (ChatbotAgent, TaskCRUDAgent)
- Reusable MCP tools
- Phased evolution (builds on Phase II)
- Quality gates (testing required)
- Event-driven preparation (async patterns)
- Security enforced (JWT, user isolation)
