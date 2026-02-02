# AI Agents Architecture - Reusable Intelligence System

## Overview

AI TaskMaster implements a **modular, reusable AI agent system** using the **4-Agent Pipeline Pattern** for natural language processing. Each agent is designed as an independent, reusable component that can be extended or replaced without affecting other agents.

This architecture demonstrates **Reusable Intelligence** through:
- **Modular Design**: Each agent has a single, well-defined responsibility
- **Composability**: Agents can be combined in different pipelines
- **Extensibility**: New agents can be added without modifying existing ones
- **Testability**: Each agent can be tested in isolation
- **Reusability**: Agents can be used in different contexts (web, CLI, API)

---

## Architecture Pattern: 4-Agent Pipeline

```
User Message
    ↓
┌─────────────────────────────────────────────────────────┐
│  IntentClassifierAgent                                   │
│  • Parses natural language                              │
│  • Extracts intent + entities                           │
│  • Returns: {intent, confidence, entities}              │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  TaskResolutionAgent                                     │
│  • Resolves ambiguous task references                   │
│  • Performs fuzzy matching                              │
│  • Returns: {task_ids, confirmation_needed}             │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  ActionAgent                                             │
│  • Routes intent to appropriate MCP tool                │
│  • Executes CRUD operations                             │
│  • Returns: {success, data, error}                      │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  ResponseFormatterAgent                                  │
│  • Formats response in natural language                 │
│  • Adds helpful context                                 │
│  • Returns: {response, metadata}                        │
└─────────────────────────────────────────────────────────┘
    ↓
Natural Language Response to User
```

---

## Agent 1: IntentClassifierAgent

**Location**: `backend/src/agents/intent_classifier.py`

### Responsibility
Classify user messages into structured intents and extract relevant entities.

### Capabilities
- **Primary**: Google Gemini 2.0 Flash Lite API for AI-powered classification
- **Fallback**: Rule-based classifier with typo normalization
- **Confidence scoring**: Returns 0.0-1.0 confidence scores
- **Low-confidence handling**: Falls back to rule-based when confidence < 0.7

### Supported Intents
| Intent | Description | Example |
|--------|-------------|---------|
| `create_task` | Create new task | "remind me to buy milk" |
| `list_tasks` | Query tasks | "show my tasks" |
| `update_task` | Modify existing task | "update task 5 to high priority" |
| `delete_task` | Remove task | "delete the grocery task" |
| `complete_task` | Mark task done | "mark buy milk as done" |
| `unclear` | Cannot determine intent | "hello" |

### Entity Extraction
```python
{
    "intent": "create_task",
    "confidence": 0.95,
    "entities": {
        "title": "buy milk",
        "priority": "high",
        "due_date": "2026-02-01",
        "tags": ["groceries"]
    }
}
```

### Reusability Features
- **API Agnostic**: Can swap Gemini for OpenAI, Anthropic, etc.
- **Conversation History Support**: Maintains context across messages
- **Extensible Intent Set**: Add new intents without breaking existing code
- **Fallback Strategy**: Graceful degradation when AI unavailable

### Usage Example
```python
from src.agents.intent_classifier import IntentClassifierAgent

agent = IntentClassifierAgent()
result = agent.classify(
    message="remind me to call mom tomorrow",
    user_id="user-123",
    correlation_id="req-abc"
)

print(result["intent"])  # "create_task"
print(result["entities"]["title"])  # "call mom"
```

---

## Agent 2: TaskResolutionAgent

**Location**: `backend/src/agents/task_resolution.py`

### Responsibility
Resolve ambiguous task references to specific task IDs using semantic matching.

### Capabilities
- **Fuzzy Matching**: Word-overlap algorithm for partial matches
- **Semantic Understanding**: Resolves "the grocery one", "first task", etc.
- **Confirmation Flow**: Returns multiple matches when ambiguous
- **MCP Integration**: Uses `list_tasks` tool for context

### Matching Algorithm

**Word-Overlap Scoring**:
```python
reference = "grocery"
tasks = [
    {"id": 5, "title": "Buy groceries at store"},
    {"id": 12, "title": "Grocery shopping list"}
]

# Algorithm:
# 1. Extract words from reference
# 2. Calculate overlap ratio with each task title
# 3. Sort by score (highest first)
# 4. Return matches with score > threshold
```

### Resolution Cases

| Input | Output | Notes |
|-------|--------|-------|
| `task_id: 5` | `[5]` | Explicit ID, direct resolution |
| `"grocery"` | `[5]` | Single match, auto-resolve |
| `"buy"` | `[5, 8, 12]` | Multiple matches, request confirmation |
| `"invalid"` | `[]` | No matches, return empty |

### Reusability Features
- **MCP Tool Integration**: Can work with any task storage backend
- **Pluggable Matching**: Easy to add different matching algorithms
- **Confirmation Protocol**: Standard format for user confirmation
- **Context-Aware**: Uses user's full task list for resolution

### Usage Example
```python
from src.agents.task_resolution import TaskResolutionAgent

agent = TaskResolutionAgent()
result = agent.resolve(
    db=session,
    user_id="user-123",
    entities={"task_reference": "grocery"},
    correlation_id="req-abc"
)

if result["confirmation_needed"]:
    # Show user: "Did you mean: Buy groceries (ID: 5) or Grocery shopping (ID: 12)?"
    pass
else:
    task_id = result["task_ids"][0]  # Use resolved ID
```

---

## Agent 3: ActionAgent

**Location**: `backend/src/agents/action_agent.py`

### Responsibility
Execute MCP tool operations based on classified intent and resolved parameters.

### Capabilities
- **Intent Routing**: Maps intents to appropriate MCP tools
- **Parameter Validation**: Ensures required fields present
- **User Isolation**: All operations filtered by user_id
- **Error Handling**: Graceful failures with helpful messages

### MCP Tool Mapping

| Intent | MCP Tool | Parameters |
|--------|----------|------------|
| `create_task` | `add_task()` | title, priority, due_date, tags |
| `list_tasks` | `list_tasks()` | completed, priority, tags |
| `update_task` | `update_task()` | task_id, title, priority, etc. |
| `delete_task` | `delete_task()` | task_id |
| `complete_task` | `complete_task()` | task_id |

### Execution Flow
```python
1. Validate intent is supported
2. Resolve task references (if needed)
3. Validate required parameters exist
4. Call appropriate MCP tool
5. Return standardized result
```

### Reusability Features
- **Tool Abstraction**: MCP tools can be swapped/extended
- **Validation Layer**: Centralized parameter validation
- **Error Normalization**: Consistent error format across tools
- **Retry Logic**: Automatic retry for transient failures

### Usage Example
```python
from src.agents.action_agent import ActionAgent

agent = ActionAgent()
result = agent.execute(
    db=session,
    intent="create_task",
    parameters={
        "title": "Buy milk",
        "priority": "high"
    },
    user_id="user-123",
    correlation_id="req-abc"
)

if result["success"]:
    print(f"Created task: {result['task']['title']}")
```

---

## Agent 4: ResponseFormatterAgent

**Location**: `backend/src/agents/response_formatter.py`

### Responsibility
Format MCP tool results into natural language responses with helpful context.

### Capabilities
- **Natural Language Generation**: Friendly, conversational responses
- **Context-Aware**: Adapts tone based on operation success/failure
- **Metadata Inclusion**: Adds task IDs, counts, next steps
- **Error Translation**: Converts technical errors to user-friendly messages

### Response Templates

**Create Task Success**:
```
Input: {"success": True, "task": {"id": 5, "title": "Buy milk"}}
Output: "✓ Created task: 'Buy milk' (ID: 5). I've added it to your list!"
```

**List Tasks**:
```
Input: {"success": True, "tasks": [...], "count": 3}
Output: "You have 3 task(s):
1. [○] Buy milk (ID: 5)
2. [✓] Call mom (ID: 6)
3. [○] Pay bills (ID: 7)"
```

**Error Handling**:
```
Input: {"success": False, "error": "Task not found"}
Output: "I couldn't find that task. Try listing your tasks first with 'show my tasks'."
```

### Reusability Features
- **Template System**: Easy to add new response patterns
- **Localization Ready**: Templates can be swapped for different languages
- **Emoji Support**: Optional emoji for visual feedback
- **Metadata Passthrough**: Returns original data for client use

### Usage Example
```python
from src.agents.response_formatter import ResponseFormatterAgent

agent = ResponseFormatterAgent()
response = agent.format_response(
    intent="create_task",
    result={
        "success": True,
        "task": {"id": 5, "title": "Buy milk"}
    },
    metadata={"correlation_id": "req-abc"}
)

print(response["response"])
# "✓ Created task: 'Buy milk' (ID: 5). I've added it to your list!"
```

---

## Agent Orchestration: ChatbotService

**Location**: `backend/src/services/chatbot_service.py`

### Responsibility
Orchestrate the 4-agent pipeline for end-to-end conversation handling.

### Pipeline Flow
```python
class ChatbotService:
    def process_message(self, db, user_id, message, conversation_id=None):
        # 1. Load conversation history (stateless)
        history = self._load_conversation_context(db, conversation_id)

        # 2. Classify intent
        intent_result = self.intent_agent.classify(message, user_id, history)

        # 3. Resolve task references
        resolution = self.resolution_agent.resolve(
            db, user_id, intent_result["entities"]
        )

        # 4. Execute action
        action_result = self.action_agent.execute(
            db, intent_result["intent"], resolution, user_id
        )

        # 5. Format response
        response = self.formatter_agent.format_response(
            intent_result["intent"], action_result
        )

        # 6. Save conversation to database
        self._save_conversation(db, user_id, message, response, conversation_id)

        return response
```

### Key Features
- **Stateless Architecture**: No server-side session storage
- **Conversation Persistence**: All history in database
- **Error Recovery**: Each agent failure isolated
- **Logging**: Full trace with correlation IDs

---

## Reusability Patterns

### 1. Agent Replacement
Swap any agent without affecting others:
```python
# Replace Gemini with OpenAI
class OpenAIIntentClassifier(IntentClassifierAgent):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def classify(self, message, ...):
        # Use OpenAI GPT-4 instead of Gemini
        pass

# Use in ChatbotService
service = ChatbotService()
service.intent_agent = OpenAIIntentClassifier()
```

### 2. Agent Extension
Add new capabilities:
```python
class SmartTaskResolutionAgent(TaskResolutionAgent):
    def resolve(self, ...):
        # Call parent implementation
        result = super().resolve(...)

        # Add AI-powered semantic search
        if not result["task_ids"]:
            result = self._semantic_search(...)

        return result
```

### 3. Custom Pipelines
Create specialized workflows:
```python
# Simple pipeline (no task resolution)
class SimpleChatbot:
    def __init__(self):
        self.classifier = IntentClassifierAgent()
        self.action = ActionAgent()
        self.formatter = ResponseFormatterAgent()

    def process(self, message):
        intent = self.classifier.classify(message)
        result = self.action.execute(intent)
        return self.formatter.format_response(result)
```

### 4. Testing Isolation
Test each agent independently:
```python
def test_intent_classifier():
    agent = IntentClassifierAgent()
    result = agent.classify("buy milk")
    assert result["intent"] == "create_task"
    assert result["entities"]["title"] == "buy milk"
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Model** | Google Gemini 2.0 Flash Lite | Intent classification, entity extraction |
| **Fallback** | Rule-based classifier | Typo normalization, keyword matching |
| **Database** | Neon PostgreSQL | Conversation history persistence |
| **ORM** | SQLModel | Type-safe database operations |
| **API** | FastAPI | RESTful endpoints for chat |
| **MCP Tools** | Internal wrappers | Phase II CRUD operations |
| **Logging** | Python logging + correlation IDs | Distributed tracing |

---

## Benefits of This Architecture

### ✅ Modularity
Each agent is an independent module with clear boundaries.

### ✅ Reusability
Agents can be used in different contexts:
- Web chat interface
- CLI application
- Mobile app
- Slack/Discord bot
- Voice assistant

### ✅ Testability
Each agent can be unit tested in isolation without dependencies.

### ✅ Maintainability
Bug fixes and improvements are localized to specific agents.

### ✅ Extensibility
New features can be added without modifying existing agents:
- Add sentiment analysis agent
- Add context enrichment agent
- Add multi-language translation agent

### ✅ Scalability
Agents can be deployed independently:
- IntentClassifier → Serverless function
- ActionAgent → Kubernetes pod
- ResponseFormatter → Edge compute

---

## Performance Characteristics

| Agent | Latency | Bottleneck | Optimization |
|-------|---------|------------|--------------|
| IntentClassifier | ~500ms | Gemini API call | Caching, batch requests |
| TaskResolution | ~50ms | Database query | Index on title field |
| ActionAgent | ~100ms | MCP tool execution | Connection pooling |
| ResponseFormatter | ~10ms | String formatting | Template caching |
| **Total Pipeline** | **~660ms** | AI inference | Async processing |

---

## Future Enhancements

### Planned Improvements
- [ ] **Caching**: Cache common intent classifications
- [ ] **Async Processing**: Non-blocking agent pipeline
- [ ] **Batch Operations**: Support multiple tasks in one message
- [ ] **Context Enrichment**: Add user preferences, task statistics
- [ ] **Multi-Agent Collaboration**: Agents can query each other
- [ ] **A/B Testing**: Compare different agent implementations
- [ ] **Monitoring**: Real-time agent performance metrics

---

## Conclusion

This **4-Agent Pipeline Architecture** demonstrates **Reusable Intelligence** by:
1. **Separating concerns** into independent, composable agents
2. **Enabling code reuse** across different interfaces (web, CLI, API)
3. **Supporting extensibility** through agent replacement and enhancement
4. **Facilitating testing** with isolated, mockable components
5. **Providing scalability** through independent deployment and optimization

Each agent is designed as a **reusable building block** that can be combined, extended, or replaced to create intelligent systems for various use cases beyond todo management.
