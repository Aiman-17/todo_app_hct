# Tasks: Phase III – Todo AI Chatbot

**Input**: Design documents from `specs/003-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Last Updated**: 2026-01-14 (integrated clarifications from /sp.clarify session)

**Tests**: Tests are OPTIONAL and NOT included in this task list unless explicitly requested.

**Organization**: Tasks are grouped by functional area to enable systematic implementation of the AI chatbot layer.

**Clarifications Integrated** (2026-01-14):
- Performance: p95 latency <5s for chat endpoint
- Retry logic: 1 retry with fixed 500ms delay (OpenAI API and MCP tools)
- Rate limiting: 100 requests per hour per user (NOT per minute)
- Deletion: Soft delete with deleted_at timestamp + optional async archival
- Observability: Structured logging with correlation IDs for distributed tracing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story/feature area this task belongs to (DB, MCP, AGENT, API, UI)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase III dependencies

- [ ] T001 Install OpenAI Agents SDK (openai==1.12.0) in backend/requirements.txt
- [ ] T002 [P] Install MCP SDK (mcp-sdk==0.3.0) in backend/requirements.txt
- [ ] T003 [P] Install OpenAI ChatKit in frontend/package.json
- [ ] T004 [P] Add Phase III environment variables to backend/.env.example
- [ ] T005 [P] Create backend/src/agents/ directory structure
- [ ] T006 [P] Create backend/src/mcp/ directory structure
- [ ] T007 [P] Create frontend/src/components/chat/ directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY chat feature can be implemented

**⚠️ CRITICAL**: No chat functionality can begin until this phase is complete

- [ ] T008 [DB] Create Conversation model in backend/src/models/conversation.py with SQLModel schema (include deleted_at field for soft delete)
- [ ] T009 [DB] Create Message model in backend/src/models/conversation.py with SQLModel schema (include deleted_at field for soft delete)
- [ ] T010 [DB] Generate Alembic migration for conversation and message tables (include deleted_at columns and partial indexes for active records)
- [ ] T011 [DB] Apply migration and verify tables created with indexes (verify partial indexes idx_active_conversations and idx_active_messages)
- [ ] T012 [P] [MCP] Implement add_task MCP tool in backend/src/mcp/task_tools.py
- [ ] T013 [P] [MCP] Implement list_tasks MCP tool in backend/src/mcp/task_tools.py
- [ ] T014 [P] [MCP] Implement complete_task MCP tool in backend/src/mcp/task_tools.py
- [ ] T015 [P] [MCP] Implement delete_task MCP tool in backend/src/mcp/task_tools.py
- [ ] T016 [P] [MCP] Implement update_task MCP tool in backend/src/mcp/task_tools.py
- [ ] T017 [MCP] Setup MCP tool logging infrastructure in backend/logs/mcp_tools.log with structured logging and correlation ID support
- [ ] T018 [MCP] Create MCP tool registry and configuration in backend/src/mcp/__init__.py

**Checkpoint**: Foundation ready - agent and chat implementation can now begin in parallel

---

## Phase 3: Agent Implementation (Priority: P1) 🎯

**Goal**: Implement the four specialized subagents for natural language processing

**Independent Test**: Agents can process sample messages and return expected outputs in isolation

### Subagent Implementation

- [ ] T019 [P] [AGENT] Create IntentClassifierAgent in backend/src/agents/intent_classifier.py
- [ ] T020 [P] [AGENT] Create TaskResolutionAgent in backend/src/agents/task_resolution.py
- [ ] T021 [P] [AGENT] Create ActionAgent in backend/src/agents/action_agent.py
- [ ] T022 [P] [AGENT] Create ResponseFormatterAgent in backend/src/agents/response_formatter.py
- [ ] T023 [AGENT] Implement agent orchestration in backend/src/services/chatbot_service.py
- [ ] T024 [AGENT] Add OpenAI API client configuration in backend/src/config/openai_config.py
- [ ] T025 [AGENT] Implement conversation context loading from database in chatbot_service.py
- [ ] T026 [AGENT] Implement stateless conversation flow (fetch history, process, save messages)

**Checkpoint**: Agents can process natural language and invoke MCP tools correctly

---

## Phase 4: Chat API Endpoints (Priority: P2)

**Goal**: Expose chat functionality via REST API endpoints

**Independent Test**: API endpoints respond correctly to authenticated requests with proper conversation management

### API Implementation

- [ ] T027 [P] [API] Create ChatRequest schema in backend/src/models/schemas.py
- [ ] T028 [P] [API] Create ChatResponse schema in backend/src/models/schemas.py (include correlation_id field)
- [ ] T029 [API] Implement POST /api/chat endpoint in backend/src/routes/chat.py (generate correlation ID, return in X-Correlation-ID header)
- [ ] T030 [API] Add JWT authentication middleware for chat endpoint
- [ ] T031 [API] Implement conversation creation logic (new conversation if no ID provided)
- [ ] T032 [API] Implement conversation continuation logic (load existing if ID provided)
- [ ] T033 [API] Add request validation and error handling in chat route
- [ ] T034 [P] [API] Implement GET /api/conversations endpoint in backend/src/routes/conversations.py
- [ ] T035 [P] [API] Implement GET /api/conversations/{id}/messages endpoint in backend/src/routes/conversations.py
- [ ] T036 [API] Register chat routes in backend/src/main.py FastAPI app
- [ ] T037 [API] Add CORS configuration for chat endpoints

**Checkpoint**: Chat API fully functional and accessible via HTTP requests

---

## Phase 5: Frontend Chat UI (Priority: P3)

**Goal**: Implement conversational UI using OpenAI ChatKit

**Independent Test**: Users can send messages, see responses, and view conversation history in browser

### UI Implementation

- [ ] T038 [P] [UI] Create ChatInterface component in frontend/src/components/chat/ChatInterface.tsx
- [ ] T039 [P] [UI] Create MessageBubble component in frontend/src/components/chat/MessageBubble.tsx
- [ ] T040 [P] [UI] Create InputBar component in frontend/src/components/chat/InputBar.tsx
- [ ] T041 [UI] Implement chat state management (conversation_id, messages, loading state)
- [ ] T042 [UI] Integrate ChatKit library in ChatInterface component
- [ ] T043 [UI] Implement API client for POST /api/chat in frontend/src/services/chat_service.ts
- [ ] T044 [UI] Add authentication token passing in chat API requests
- [ ] T045 [UI] Implement message rendering with role-based styling (user vs assistant)
- [ ] T046 [UI] Add loading indicators for agent responses
- [ ] T047 [UI] Implement error handling and user-friendly error messages
- [ ] T048 [UI] Create /chat route page in frontend/src/app/chat/page.tsx
- [ ] T049 [UI] Add navigation link to chat page in main layout

**Checkpoint**: Full frontend chat interface working with backend integration

---

## Phase 6: Integration & Refinement (Priority: P4)

**Goal**: End-to-end integration, error handling, and user experience improvements

**Independent Test**: Complete user flows work from login → chat → task management → logout

### Integration Tasks

- [ ] T050 [P] Implement retry logic for OpenAI API failures in chatbot_service.py (1 retry with fixed 500ms delay)
- [ ] T051 [P] Add rate limiting for chat endpoint (100 requests per hour per user)
- [ ] T052 Add conversation history pagination (load last 50 messages)
- [ ] T053 Implement low-confidence intent handling (< 0.7 threshold)
- [ ] T054 Add ambiguous task reference confirmation flow
- [ ] T055 Implement "task not found" error handling with helpful messages
- [ ] T056 Add MCP tool failure retry logic (1 retry with 500ms delay)
- [ ] T057 Implement database connection error handling with retries
- [ ] T058 [P] Add tool call metadata to chat responses for transparency
- [ ] T059 [P] Implement conversation deletion endpoint (soft delete with deleted_at timestamp, optional async archival job)
- [ ] T060 Add streaming response support for real-time chat (optional enhancement)

**Checkpoint**: Robust, production-ready chat experience with graceful error handling

---

## Phase 7: Testing & Validation (Priority: P5)

**Goal**: Comprehensive testing to ensure quality and reliability

**Independent Test**: All test suites pass with >80% coverage for MCP tools

### Testing Tasks

- [ ] T061 [P] Write unit tests for IntentClassifierAgent in backend/tests/test_intent_classifier.py
- [ ] T062 [P] Write unit tests for TaskResolutionAgent in backend/tests/test_task_resolution.py
- [ ] T063 [P] Write unit tests for ActionAgent in backend/tests/test_action_agent.py
- [ ] T064 [P] Write unit tests for ResponseFormatterAgent in backend/tests/test_response_formatter.py
- [ ] T065 [P] Write unit tests for all MCP tools in backend/tests/test_mcp_tools.py
- [ ] T066 Write integration test for full conversation flow in backend/tests/test_conversation_flow.py
- [ ] T067 [P] Write contract tests for POST /api/chat endpoint
- [ ] T068 [P] Write contract tests for GET /api/conversations endpoint
- [ ] T069 [P] Write E2E tests for chat UI in frontend/tests/chat.spec.ts
- [ ] T070 Run test coverage report and ensure ≥80% for MCP tools
- [ ] T071 Validate quickstart.md instructions (manual walkthrough)

**Checkpoint**: All tests passing, coverage targets met

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T072 [P] Update README.md with Phase III setup instructions
- [ ] T073 [P] Document MCP tool API in backend/docs/mcp-tools.md
- [ ] T074 [P] Document agent architecture in backend/docs/agents.md
- [ ] T075 Add code comments for complex agent logic
- [ ] T076 Run security audit (check JWT validation, user isolation, input sanitization)
- [ ] T077 Performance testing (verify <2s p95 latency for chat endpoint)
- [ ] T078 [P] Setup monitoring/logging for production (optional for hackathon)
- [ ] T079 Code cleanup and lint fixes across backend and frontend
- [ ] T080 Create demo video or screenshots for hackathon submission

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all feature implementation
- **Agent Implementation (Phase 3)**: Depends on Foundational (Phase 2) - specifically MCP tools
- **Chat API (Phase 4)**: Depends on Foundational (Phase 2) and Agent Implementation (Phase 3)
- **Frontend UI (Phase 5)**: Depends on Chat API (Phase 4) being functional
- **Integration (Phase 6)**: Depends on Phases 3, 4, 5 being complete
- **Testing (Phase 7)**: Can start in parallel with Phases 3-6 (TDD approach) or after implementation
- **Polish (Phase 8)**: Depends on all desired features being complete

### Task-Level Dependencies

**Database Setup (Phase 2)**:
- T008-T011 must run sequentially (model → migration → apply → verify)
- T012-T016 (MCP tools) can all run in parallel (different tools)

**Agent Implementation (Phase 3)**:
- T019-T022 (individual agents) can run in parallel
- T023-T026 (orchestration) depends on T019-T022 completing

**Chat API (Phase 4)**:
- T027-T028 (schemas) can run in parallel
- T029-T033 (chat endpoint) depends on schemas
- T034-T035 (conversation endpoints) can run in parallel with T029-T033
- T036-T037 (registration) depends on all endpoints being created

**Frontend UI (Phase 5)**:
- T038-T040 (components) can run in parallel
- T041-T047 (integration logic) depends on components
- T048-T049 (routing) depends on integration being complete

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004, T005, T006, T007 can all run in parallel

**Phase 2 (Foundational)**:
- T012-T016 (MCP tools) can run in parallel
- T018 (tool registry) can run in parallel with tool implementation

**Phase 3 (Agents)**: T019-T022 (all four agents) can run in parallel

**Phase 4 (API)**: T027-T028 (schemas), T034-T035 (conversation endpoints) can run in parallel

**Phase 5 (UI)**: T038-T040 (components) can run in parallel

**Phase 7 (Testing)**: T061-T065, T067-T069 (all unit/contract/E2E tests) can run in parallel

**Phase 8 (Polish)**: T072-T074 (documentation tasks) can run in parallel

---

## Parallel Example: MCP Tools (Phase 2)

```bash
# Launch all MCP tool implementations together:
Task: "Implement add_task MCP tool in backend/src/mcp/task_tools.py"
Task: "Implement list_tasks MCP tool in backend/src/mcp/task_tools.py"
Task: "Implement complete_task MCP tool in backend/src/mcp/task_tools.py"
Task: "Implement delete_task MCP tool in backend/src/mcp/task_tools.py"
Task: "Implement update_task MCP tool in backend/src/mcp/task_tools.py"
```

## Parallel Example: Agents (Phase 3)

```bash
# Launch all agent implementations together:
Task: "Create IntentClassifierAgent in backend/src/agents/intent_classifier.py"
Task: "Create TaskResolutionAgent in backend/src/agents/task_resolution.py"
Task: "Create ActionAgent in backend/src/agents/action_agent.py"
Task: "Create ResponseFormatterAgent in backend/src/agents/response_formatter.py"
```

---

## Implementation Strategy

### MVP First (Phases 1-5 Only)

1. Complete Phase 1: Setup → Dependencies installed
2. Complete Phase 2: Foundational → Database & MCP tools ready
3. Complete Phase 3: Agent Implementation → Agents can process messages
4. Complete Phase 4: Chat API → Backend endpoints functional
5. Complete Phase 5: Frontend UI → End-to-end chat working
6. **STOP and VALIDATE**: Test chat functionality end-to-end
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add Agent Implementation → Test agent logic with mocked MCP tools
3. Add Chat API → Test API with Postman/curl
4. Add Frontend UI → Test full user flow → Deploy/Demo (MVP!)
5. Add Integration improvements → Deploy/Demo
6. Add Testing → Ensure quality
7. Add Polish → Final deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (Phases 1-2)
2. Once Foundational is done:
   - **Developer A**: Agent Implementation (Phase 3)
   - **Developer B**: Chat API (Phase 4) - starts after Phase 3
   - **Developer C**: MCP tool testing (Phase 7, tasks T065)
3. After Phase 4 complete:
   - **Developer D**: Frontend UI (Phase 5)
4. After Phase 5 complete:
   - All team members: Integration, Testing, Polish (Phases 6-8)

---

## Notes

- [P] tasks = different files or components, no dependencies within same phase
- [Story] labels map tasks to functional areas: DB (database), MCP (tools), AGENT (subagents), API (endpoints), UI (frontend)
- Each phase should be independently completable and testable
- Tests can be written first (TDD) or after implementation (verification)
- Commit after each task or logical group
- Stop at any checkpoint to validate functionality independently
- Phase 2 (Foundational) is critical - all subsequent work depends on it
- Avoid: vague tasks, file conflicts, breaking Phase I/II existing functionality

---

## Critical Success Factors

1. **Stateless Architecture**: Ensure no server-side session storage - all state in database
2. **User Isolation**: All MCP tools MUST filter by user_id from JWT
3. **MCP-Only Database Access**: Agents NEVER query database directly
4. **Error Handling**: All errors return user-friendly messages, never raw exceptions
5. **Testing**: Especially critical for MCP tools (user isolation tests)
6. **Performance**: Chat endpoint <2s p95 latency
7. **Additive-Only**: No modifications to Phase I/II code

---

## Summary

- **Total Tasks**: 80
- **Setup Tasks**: 7 (Phase 1)
- **Foundational Tasks**: 11 (Phase 2)
- **Agent Tasks**: 8 (Phase 3)
- **API Tasks**: 11 (Phase 4)
- **UI Tasks**: 12 (Phase 5)
- **Integration Tasks**: 11 (Phase 6)
- **Testing Tasks**: 11 (Phase 7)
- **Polish Tasks**: 9 (Phase 8)
- **Parallel Opportunities**: 42 tasks marked [P] can run in parallel within their phases
- **MVP Scope**: Phases 1-5 (first 61 tasks) for functional chat demo
- **Format Validation**: ✅ All tasks follow checklist format with ID, labels, file paths
