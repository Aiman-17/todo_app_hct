# Research: Phase III – Todo AI Chatbot

**Phase**: Phase III - AI Conversational Layer
**Date**: 2026-01-13
**Purpose**: Technology decisions and best practices for AI chatbot implementation

## Executive Summary

Phase III integrates conversational AI into the todo application using OpenAI Agents SDK for natural language processing and MCP (Model Context Protocol) for database operations. Key decisions include stateless architecture with database-backed conversation history, subagent pattern for separation of concerns, and MCP tools for strict database access control.

## 1. OpenAI Agents SDK vs Alternatives

### Decision: OpenAI Agents SDK

**Rationale**:
- Official SDK provides stable, well-documented API for agent orchestration
- Built-in support for tool calling (essential for MCP integration)
- Streaming responses for better UX
- Conversation management utilities
- Strong community support and regular updates

**Alternatives Considered**:
1. **LangChain**
   - Pros: Extensive ecosystem, many integrations
   - Cons: Heavyweight, complex abstraction layers, overkill for simple task management
   - Rejected: Too much overhead for Phase III requirements

2. **Direct OpenAI API**
   - Pros: Maximum control, minimal dependencies
   - Cons: Manual conversation state management, manual tool calling logic
   - Rejected: Requires significant boilerplate that Agents SDK provides

3. **Anthropic Claude API**
   - Pros: Strong reasoning capabilities, function calling support
   - Cons: Different API patterns, less documentation for Python
   - Rejected: Spec explicitly requests OpenAI Agents SDK

**Best Practices**:
- Use async/await for all SDK calls (non-blocking I/O)
- Implement retry logic: 1 retry with fixed 500ms delay (per clarification)
- Stream responses to frontend for real-time feedback
- Cache system prompts to reduce token usage
- Target p95 latency: <5 seconds including API processing time

## 2. MCP (Model Context Protocol) Implementation

### Decision: Official MCP SDK with Custom Tool Wrappers

**Rationale**:
- MCP provides standardized interface between agents and database
- Enforces user isolation (all tools require user_id parameter)
- Enables audit logging for every database operation
- Prepares for Phase IV event-driven architecture (MCP logs → Kafka)
- Prevents agents from directly accessing database (security boundary)

**Alternatives Considered**:
1. **Direct Database Access from Agents**
   - Pros: Simpler, fewer layers
   - Cons: Violates constitution's MCP-only requirement, security risk (no isolation enforcement)
   - Rejected: Explicitly prohibited by CLAUDE-PHASE3.md

2. **REST API Calls from Agents**
   - Pros: Uses existing Phase II endpoints
   - Cons: HTTP overhead, latency, no strong typing, circular dependency (API → Agent → API)
   - Rejected: Performance overhead, architectural complexity

3. **Custom Protocol**
   - Pros: Tailored to specific needs
   - Cons: Reinventing wheel, maintenance burden
   - Rejected: MCP SDK provides everything needed

**Best Practices**:
- Each MCP tool validates parameters before database access
- Tools return structured responses: `{success: bool, data: dict, error: str | null}`
- Idempotent operations (e.g., completing completed task is no-op)
- Comprehensive logging: `{timestamp, user_id, tool, parameters, result, latency_ms}`

## 3. Stateless Architecture Pattern

### Decision: Database-Backed Conversation History

**Rationale**:
- Enables horizontal scaling (no sticky sessions required)
- Conversation persistence across server restarts
- Audit trail for all interactions
- Single source of truth (database)
- Simplified deployment (no Redis/memcached dependency)

**Alternatives Considered**:
1. **In-Memory Session Storage**
   - Pros: Fast access
   - Cons: Lost on restart, doesn't scale horizontally, violates stateless requirement
   - Rejected: Constitution requires stateless architecture

2. **Redis Session Store**
   - Pros: Fast, distributed
   - Cons: Additional infrastructure, cache invalidation complexity, cost
   - Rejected: Overengineering for Phase III (100 concurrent sessions)

3. **Client-Side Storage**
   - Pros: No server storage needed
   - Cons: Security risk (JWT tokens in localStorage), large payloads, no server-side audit
   - Rejected: Security and compliance concerns

**Best Practices**:
- Fetch conversation history on every request (SELECT messages WHERE conversation_id = ?)
- Limit history to last 50 messages (pagination for longer conversations)
- Append-only message table (never UPDATE or DELETE messages)
- Index on (conversation_id, created_at) for fast retrieval

## 4. Subagent Architecture

### Decision: Four Specialized Subagents

**Rationale**:
- Separation of concerns (single responsibility principle)
- Testable in isolation
- Reusable components
- Clear failure points

**Subagents**:

#### 4.1 IntentClassifierAgent
- **Purpose**: Parse user message → intent + entities
- **Input**: Raw message string
- **Output**: `{intent: str, confidence: float, entities: dict}`
- **Tools**: None (pure classification)
- **Confidence Threshold**: >0.7 for execution, <0.7 request clarification

#### 4.2 TaskResolutionAgent
- **Purpose**: Resolve ambiguous task references ("the first one", "my grocery task")
- **Input**: Entities dict + user_id
- **Output**: `{task_ids: [int], confirmation_needed: bool}`
- **Tools**: list_tasks (read-only)
- **Rules**: Always confirm if multiple matches

#### 4.3 ActionAgent
- **Purpose**: Execute MCP tools based on intent
- **Input**: Intent + parameters + user_id
- **Output**: MCP tool result
- **Tools**: All 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Rules**: Validate parameters, enforce user_id, handle errors gracefully

#### 4.4 ResponseFormatterAgent
- **Purpose**: Convert MCP output → user-friendly response
- **Input**: Tool output JSON
- **Output**: Natural language string
- **Tools**: None (pure formatting)
- **Rules**: Concise, conversational, confirm actions

**Alternatives Considered**:
1. **Single Monolithic Agent**
   - Pros: Simpler codebase
   - Cons: Hard to test, unclear failure modes, mixed responsibilities
   - Rejected: Violates single responsibility principle

2. **Agent per MCP Tool (5+ agents)**
   - Pros: Maximum granularity
   - Cons: Overengineering, coordination complexity
   - Rejected: Unnecessary complexity for Phase III

**Best Practices**:
- Each subagent has clear input/output contract
- Subagents don't call each other (orchestrated by chatbot_service.py)
- Unit test each subagent independently
- Integration tests verify full pipeline

## 5. Frontend: OpenAI ChatKit vs Alternatives

### Decision: OpenAI ChatKit

**Rationale**:
- Official React component library from OpenAI
- Built-in support for streaming responses
- Accessible UI (ARIA labels, keyboard navigation)
- Matches brand expectations for AI chat
- Well-documented, actively maintained

**Alternatives Considered**:
1. **Custom Chat UI**
   - Pros: Full control, no external dependency
   - Cons: Accessibility complexity, streaming implementation, maintenance burden
   - Rejected: Reinventing wheel, Phase III timeline

2. **react-chatbot-kit**
   - Pros: Open source, flexible
   - Cons: Not optimized for LLM streaming, fewer updates
   - Rejected: ChatKit is better maintained

3. **shadcn/ui + Custom Components**
   - Pros: Consistent with Phase II UI
   - Cons: Manual streaming, message management
   - Rejected: ChatKit provides everything needed

**Best Practices**:
- Integrate with existing shadcn/ui theme
- Add loading states for streaming responses
- Display MCP tool calls for transparency
- Implement error boundaries for graceful failures

## 6. Database Schema Design

### Decision: Two New Tables (Conversation, Message)

**Rationale**:
- Minimal schema extension to Phase II
- Conversation groups related messages
- Message is append-only (audit trail)
- Foreign keys ensure referential integrity

**Schema**:

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  INDEX idx_user_conversations (user_id, created_at DESC)
);

CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  INDEX idx_conversation_messages (conversation_id, created_at ASC)
);
```

**Alternatives Considered**:
1. **Single Table (Conversation + Messages)**
   - Pros: Simpler schema
   - Cons: Sparse columns, harder to query
   - Rejected: Poor normalization

2. **Separate Tables per User**
   - Pros: Isolation
   - Cons: Schema management nightmare, doesn't scale
   - Rejected: Anti-pattern

**Best Practices**:
- Use UUIDs for conversation_id (prevents enumeration attacks)
- Add updated_at trigger on conversations table
- Soft delete conversations with deleted_at timestamp (per clarification)
- Optional asynchronous archival job MAY copy soft-deleted data to archived_* tables
- Partition messages table if >10M rows (future optimization)

## 7. Error Handling Strategy

### Decision: Graceful Degradation with User-Friendly Messages

**Rationale**:
- Users should never see raw error messages
- Low confidence intent → clarification request (not error)
- MCP tool failures → retry once, then user notification
- Database errors → generic "try again" message

**Error Categories**:

1. **Low Confidence Intent** (<0.7)
   - Response: "I'm not sure what you want to do. Try: 'show my tasks' or 'create a new task'"

2. **Task Not Found**
   - Response: "I couldn't find task #999. Try 'show my tasks' to see your list."

3. **Ambiguous Reference**
   - Response: "You have multiple tasks matching 'meeting'. Which one? 1) Team meeting 2) Client meeting"

4. **MCP Tool Failure**
   - Retry: 1 attempt with fixed 500ms delay (per clarification)
   - Response: "I'm having trouble connecting to the database. Please try again in a moment."

5. **OpenAI API Failure**
   - Retry: 1 attempt with fixed 500ms delay (per clarification)
   - Response: "I'm having trouble processing your request. Please try again."

6. **Database Connection Error**
   - Retry: 1 attempt with 500ms delay
   - Response: "Service temporarily unavailable. Please try again later."

**Best Practices**:
- Log all errors with stack traces (backend logs only)
- Never expose internal details to users
- Provide actionable next steps in error messages
- Monitor error rates (alert if >5% of requests fail)

## 8. Testing Strategy

### Decision: Three-Layer Testing Pyramid

**Rationale**:
- Unit tests (70%): Fast, isolated, many
- Integration tests (20%): Verify subagent coordination
- E2E tests (10%): Critical user flows

**Test Layers**:

#### 8.1 Unit Tests (pytest)
```python
# tests/test_intent_classifier.py
def test_create_task_intent():
    agent = IntentClassifierAgent()
    result = agent.classify("remind me to call mom")
    assert result["intent"] == "create_task"
    assert result["confidence"] > 0.7
```

#### 8.2 Integration Tests
```python
# tests/test_conversation_flow.py
def test_full_conversation_flow(client, auth_headers):
    response = client.post("/api/chat",
        json={"message": "add task: buy milk"},
        headers=auth_headers
    )
    assert "Created task" in response.json()["response"]
```

#### 8.3 E2E Tests (Playwright)
```typescript
// tests/e2e/chat.spec.ts
test('user can create task via chat', async ({ page }) => {
  await page.fill('[data-testid="chat-input"]', 'remind me to call dentist');
  await page.click('[data-testid="chat-send"]');
  await expect(page.locator('.chat-message').last()).toContainText('Created task');
});
```

**Best Practices**:
- Mock OpenAI API in unit tests (use recorded responses)
- Use in-memory SQLite for integration tests (faster)
- Run E2E tests against staging environment
- Coverage target: 80% for MCP tools, 60% overall

## 9. Performance Optimization

### Decision: Lazy Loading + Database Indexing

**Optimizations**:

1. **Database Indexing**
   - Index: `(conversation_id, created_at)` on messages
   - Index: `(user_id, created_at DESC)` on conversations
   - Expected: <100ms for conversation history queries

2. **Lazy Loading**
   - Load last 50 messages only
   - Pagination for older messages
   - Reduces payload size by 90% for long conversations

3. **Connection Pooling**
   - Use SQLModel's connection pool (min=5, max=20)
   - Prevents connection exhaustion under load

4. **Async/Await**
   - All I/O operations use async/await
   - Concurrent MCP tool calls when possible

**Performance Targets**:
- Chat endpoint: <2s p95 latency
- Database queries: <100ms p95
- Concurrent sessions: 100 without degradation

**Best Practices**:
- Profile with Locust (load testing tool)
- Monitor with Prometheus + Grafana (future phases)
- Add query logging in development (detect slow queries)

## 10. Security Considerations

### Decision: Defense in Depth

**Security Layers**:

1. **Authentication**
   - JWT validation on every chat request
   - Extract user_id from token (never from request body)
   - Reject expired tokens (Better Auth handles this)

2. **Authorization**
   - All MCP tools enforce user_id filtering
   - Users can only access their own tasks/conversations
   - No cross-user data leakage possible

3. **Input Sanitization**
   - Validate all user messages (max length: 2000 chars)
   - Escape SQL in raw queries (use parameterized queries)
   - Prevent injection in natural language inputs

4. **Rate Limiting**
   - 100 requests/minute per user (prevents abuse)
   - Implemented in FastAPI middleware

5. **Secrets Management**
   - OpenAI API key in environment variable (OPENAI_API_KEY)
   - Never log API keys or JWT tokens
   - Rotate keys quarterly

**Best Practices**:
- Follow OWASP Top 10 guidelines
- Regular security audits (AuthenticationAgent responsibility)
- Log all security events (failed auth, rate limits)
- HTTPS enforced in production (Phase IV+)

## 11. Rate Limiting & Security (Post-Clarification)

### Decision: 100 Requests Per Hour Per User

**Rationale** (from /sp.clarify session 2026-01-14):
- Prevents abuse while allowing natural conversation flow (~1.67 requests/minute)
- More generous than strict per-minute limits
- Still provides protection against automated spam
- Appropriate for chatbot interface where users type and wait for responses

**Implementation**:
- Use sliding window counter in Redis (or in-memory for Phase III)
- Key format: `ratelimit:chat:{user_id}`
- Return 429 Too Many Requests when limit exceeded
- Include `Retry-After` header with seconds until reset

**Best Practices**:
- Exclude failed auth attempts from rate limit (prevent lockout)
- Log rate limit violations for abuse monitoring
- Allow burst handling (up to 10 requests in 1 minute, then throttle to hourly limit)

## 12. Observability Strategy (Post-Clarification)

### Decision: Structured Logging with Correlation IDs

**Rationale** (from /sp.clarify session 2026-01-14):
- Enables end-to-end request tracing through distributed system
- Correlation IDs link: API request → Agent → MCP tools → Database queries
- Essential for debugging issues in multi-layer architecture
- Lighter weight than full tracing (OpenTelemetry) for Phase III scale
- Prepares for metrics dashboard addition in Phase IV

**Implementation**:
```python
# Generate correlation ID at API entry point
correlation_id = str(uuid4())

# Propagate through all layers
logger.info("Chat request received", extra={
    "correlation_id": correlation_id,
    "user_id": user_id,
    "conversation_id": conversation_id,
    "timestamp": datetime.utcnow().isoformat(),
    "latency_ms": elapsed_ms
})
```

**Log Structure**:
- **Level INFO**: All successful requests/responses
- **Level WARN**: Retry attempts (OpenAI API, MCP tools)
- **Level ERROR**: Failures with stack traces

**Logged Fields**:
- `correlation_id`: Request trace ID
- `user_id`: Authenticated user
- `conversation_id`: Conversation context
- `timestamp`: ISO 8601 format
- `latency_ms`: Operation duration
- `tool_name`: MCP tool invoked (if applicable)
- `parameters`: Tool input (sanitized, no PII)
- `result`: Tool output summary
- `error`: Error message (if failure)

**Best Practices**:
- Use structured logging library (Python: `structlog`, TypeScript: `pino`)
- Sanitize logs: remove passwords, tokens, PII
- Rotate logs daily, retain 30 days
- Centralized logging in Phase IV (ELK stack or CloudWatch)

## Research Conclusions

All technology decisions are finalized and aligned with:
- Phase III specification requirements
- Project constitution principles
- Industry best practices
- Clarifications from /sp.clarify session 2026-01-14:
  - Performance: p95 latency <5s
  - Resilience: 1 retry with 500ms delay for OpenAI/MCP failures
  - Rate limiting: 100 requests/hour per user
  - Deletion: Soft delete with optional async archival
  - Observability: Structured logging with correlation IDs

**Ready to proceed to Phase 1: Design & Contracts**
