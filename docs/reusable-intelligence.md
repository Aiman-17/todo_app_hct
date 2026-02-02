# Reusable Intelligence - Design Patterns & Implementation Guide

## What is Reusable Intelligence?

**Reusable Intelligence** refers to AI components designed to be:
- **Modular**: Independent units with clear interfaces
- **Composable**: Can be combined in different configurations
- **Portable**: Work across different platforms and contexts
- **Extensible**: Easy to enhance without breaking existing functionality
- **Testable**: Can be validated in isolation

AI TaskMaster implements Reusable Intelligence through **Claude Code Subagents and Agent Skills**, enabling AI-powered functionality to be reused across different contexts, platforms, and applications.

---

## Core Design Principles

### 1. Single Responsibility Principle
Each agent has exactly one reason to change:
- **IntentClassifierAgent**: Only handles intent classification
- **TaskResolutionAgent**: Only handles task reference resolution
- **ActionAgent**: Only handles MCP tool execution
- **ResponseFormatterAgent**: Only handles response formatting

### 2. Interface Segregation
Agents expose minimal, well-defined interfaces:
```python
class IntentClassifierAgent:
    def classify(message: str, ...) -> dict:
        """Single public method, clear contract."""
        pass
```

### 3. Dependency Inversion
Agents depend on abstractions (MCP tools), not concrete implementations:
```python
class ActionAgent:
    def execute(self, db, intent, parameters, user_id):
        # Uses MCP tool abstraction
        result = add_task(db, user_id, **parameters)
```

### 4. Open/Closed Principle
Open for extension, closed for modification:
```python
# Extend without modifying original
class EnhancedIntentClassifier(IntentClassifierAgent):
    def classify(self, message, ...):
        result = super().classify(message, ...)
        # Add sentiment analysis
        result["sentiment"] = self._analyze_sentiment(message)
        return result
```

---

## Reusability Patterns

### Pattern 1: Agent Substitution

Replace any agent with an alternative implementation:

**Example: Swap Gemini for OpenAI**
```python
# Original (Gemini-based)
from src.agents.intent_classifier import IntentClassifierAgent

# Alternative (OpenAI-based)
class OpenAIIntentClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4"

    def classify(self, message: str, ...) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        return self._parse_response(response)

# Use in service
chatbot = ChatbotService()
chatbot.intent_agent = OpenAIIntentClassifier()  # Swap implementation
```

**Why this works:**
- Both implementations have the same `classify()` signature
- ChatbotService doesn't know (or care) which implementation is used
- Zero changes to other agents or service code

---

### Pattern 2: Agent Composition

Combine agents in different configurations:

**Example: Create a Simple Chatbot (No Task Resolution)**
```python
class SimpleChatbot:
    """Lightweight chatbot without fuzzy matching."""
    def __init__(self):
        self.classifier = IntentClassifierAgent()
        self.action = ActionAgent()
        self.formatter = ResponseFormatterAgent()

    def process(self, db, user_id, message):
        # 3-agent pipeline (skip task resolution)
        intent_result = self.classifier.classify(message, user_id)
        action_result = self.action.execute(db, intent_result["intent"],
                                           intent_result["entities"], user_id)
        response = self.formatter.format_response(intent_result["intent"], action_result)
        return response
```

**Example: Create an Advanced Chatbot (Add Context Agent)**
```python
class AdvancedChatbot:
    """Chatbot with user context enrichment."""
    def __init__(self):
        self.context_agent = UserContextAgent()  # NEW
        self.classifier = IntentClassifierAgent()
        self.resolution = TaskResolutionAgent()
        self.action = ActionAgent()
        self.formatter = ResponseFormatterAgent()

    def process(self, db, user_id, message):
        # 5-agent pipeline (add context enrichment)
        context = self.context_agent.enrich(db, user_id)  # Get user preferences, stats
        intent_result = self.classifier.classify(message, user_id, context)
        resolution = self.resolution.resolve(db, user_id, intent_result["entities"])
        action_result = self.action.execute(db, intent_result["intent"], resolution, user_id)
        response = self.formatter.format_response(intent_result["intent"], action_result, context)
        return response
```

---

### Pattern 3: Agent Enhancement

Add capabilities to existing agents without modification:

**Example: Add Caching to Intent Classifier**
```python
class CachedIntentClassifier(IntentClassifierAgent):
    def __init__(self):
        super().__init__()
        self.cache = {}  # Simple in-memory cache

    def classify(self, message: str, ...) -> dict:
        # Check cache first
        cache_key = message.lower().strip()
        if cache_key in self.cache:
            logger.info("IntentClassifier: cache hit")
            return self.cache[cache_key]

        # Call parent implementation
        result = super().classify(message, ...)

        # Store in cache
        self.cache[cache_key] = result
        return result
```

**Example: Add Logging to Action Agent**
```python
class LoggedActionAgent(ActionAgent):
    def execute(self, db, intent, parameters, user_id, correlation_id=None):
        start_time = time.time()
        logger.info(f"ActionAgent: executing {intent}", extra={
            "user_id": user_id,
            "correlation_id": correlation_id
        })

        # Call parent implementation
        result = super().execute(db, intent, parameters, user_id, correlation_id)

        elapsed = time.time() - start_time
        logger.info(f"ActionAgent: completed {intent} in {elapsed:.2f}s")
        return result
```

---

### Pattern 4: Cross-Platform Reuse

Use the same agents across different interfaces:

**Web API (FastAPI)**
```python
# backend/src/routes/chat.py
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    service = ChatbotService()
    response = service.process_message(db, user_id, request.message)
    return response
```

**CLI Application**
```python
# cli/chatbot.py
def main():
    service = ChatbotService()
    while True:
        message = input("You: ")
        response = service.process_message(db, user_id, message)
        print(f"Bot: {response['response']}")
```

**Slack Bot**
```python
# integrations/slack_bot.py
@app.event("message")
def handle_message(event, say):
    service = ChatbotService()
    response = service.process_message(db, event["user"], event["text"])
    say(response["response"])
```

**Voice Assistant**
```python
# integrations/voice_assistant.py
def process_voice_command(audio):
    transcript = speech_to_text(audio)
    service = ChatbotService()
    response = service.process_message(db, user_id, transcript)
    text_to_speech(response["response"])
```

**Same agents, different interfaces!**

---

## Real-World Reusability Examples

### Example 1: Multi-Tenant SaaS

Reuse agents across different customer deployments:

```python
class TenantAwareChatbot(ChatbotService):
    def process_message(self, db, user_id, message, tenant_id):
        # Load tenant configuration
        config = get_tenant_config(tenant_id)

        # Use tenant-specific AI model
        if config["ai_provider"] == "openai":
            self.intent_agent = OpenAIIntentClassifier()
        else:
            self.intent_agent = IntentClassifierAgent()  # Gemini

        # Process with tenant isolation
        return super().process_message(db, user_id, message)
```

### Example 2: Multi-Language Support

Reuse agents with different language models:

```python
class MultilingualChatbot(ChatbotService):
    def process_message(self, db, user_id, message, language="en"):
        # Use language-specific formatter
        if language == "ur":
            self.formatter = UrduResponseFormatter()
        elif language == "es":
            self.formatter = SpanishResponseFormatter()
        else:
            self.formatter = ResponseFormatterAgent()  # English

        return super().process_message(db, user_id, message)
```

### Example 3: A/B Testing

Test different agent implementations:

```python
class ABTestingChatbot(ChatbotService):
    def process_message(self, db, user_id, message):
        # Randomly assign user to test group
        test_group = hash(user_id) % 2

        if test_group == 0:
            # Control: Gemini
            self.intent_agent = IntentClassifierAgent()
        else:
            # Variant: OpenAI
            self.intent_agent = OpenAIIntentClassifier()

        # Track which variant was used
        result = super().process_message(db, user_id, message)
        result["test_group"] = test_group
        return result
```

---

## Testing Reusable Intelligence

### Unit Testing Agents

Test each agent in isolation:

```python
def test_intent_classifier():
    """Test IntentClassifierAgent independently."""
    agent = IntentClassifierAgent()

    # Test create_task intent
    result = agent.classify("remind me to buy milk")
    assert result["intent"] == "create_task"
    assert result["entities"]["title"] == "buy milk"

    # Test list_tasks intent
    result = agent.classify("show my tasks")
    assert result["intent"] == "list_tasks"

def test_task_resolution():
    """Test TaskResolutionAgent independently."""
    agent = TaskResolutionAgent()

    # Mock database with test data
    db = create_test_db([
        {"id": 5, "title": "Buy groceries"},
        {"id": 12, "title": "Call mom"}
    ])

    # Test fuzzy matching
    result = agent.resolve(db, "user-123", {"task_reference": "grocery"})
    assert result["task_ids"] == [5]
    assert not result["confirmation_needed"]
```

### Integration Testing Pipeline

Test agent collaboration:

```python
def test_chatbot_pipeline():
    """Test full 4-agent pipeline."""
    service = ChatbotService()

    # Test create task flow
    response = service.process_message(
        db=test_db,
        user_id="user-123",
        message="add a task to buy milk"
    )

    assert response["intent"] == "create_task"
    assert "buy milk" in response["response"]
    assert response["metadata"]["task_id"] is not None
```

### Mocking Agents

Replace agents with mocks for testing:

```python
class MockIntentClassifier:
    """Mock classifier for testing."""
    def classify(self, message, ...):
        return {
            "intent": "create_task",
            "confidence": 1.0,
            "entities": {"title": "test task"}
        }

def test_with_mock():
    service = ChatbotService()
    service.intent_agent = MockIntentClassifier()  # Inject mock

    response = service.process_message(db, "user-123", "any message")
    # Predictable behavior for testing
```

---

## Performance Optimization

### Caching Strategies

**Intent Classification Cache**:
```python
# Cache common queries
CACHE = {
    "show my tasks": {"intent": "list_tasks", "confidence": 1.0},
    "what are my tasks": {"intent": "list_tasks", "confidence": 1.0},
}
```

**Task Resolution Cache**:
```python
# Cache recent task lookups
task_cache = TTLCache(maxsize=100, ttl=300)  # 5-minute TTL
```

### Async Processing

Make agents non-blocking:

```python
class AsyncChatbotService:
    async def process_message(self, db, user_id, message):
        # Run agents concurrently where possible
        intent_task = asyncio.create_task(
            self.intent_agent.classify_async(message)
        )
        context_task = asyncio.create_task(
            self._load_conversation_context(db, conversation_id)
        )

        intent_result, context = await asyncio.gather(intent_task, context_task)
        # Continue pipeline...
```

---

## Best Practices

### ✅ DO: Keep Agents Stateless
```python
# Good: No instance state
class IntentClassifierAgent:
    def classify(self, message):
        # All state passed as parameters
        pass
```

### ❌ DON'T: Store State in Agents
```python
# Bad: Instance state breaks reusability
class BadIntentClassifier:
    def __init__(self):
        self.last_message = None  # ❌ Shared state

    def classify(self, message):
        self.last_message = message  # ❌ Side effects
```

### ✅ DO: Use Dependency Injection
```python
# Good: Dependencies passed in
class ChatbotService:
    def __init__(self, intent_agent=None, action_agent=None):
        self.intent_agent = intent_agent or IntentClassifierAgent()
        self.action_agent = action_agent or ActionAgent()
```

### ❌ DON'T: Hardcode Dependencies
```python
# Bad: Hardcoded dependencies
class BadChatbot:
    def __init__(self):
        self.agent = IntentClassifierAgent()  # ❌ Can't swap
```

### ✅ DO: Return Structured Data
```python
# Good: Predictable structure
def classify(self, message) -> dict:
    return {
        "intent": "create_task",
        "confidence": 0.95,
        "entities": {...}
    }
```

### ❌ DON'T: Return Inconsistent Types
```python
# Bad: Unpredictable return type
def classify(self, message):
    if success:
        return {"intent": "..."}
    else:
        return None  # ❌ Inconsistent
```

---

## Migration Guide

### From Monolithic to Agents

**Before (Monolithic)**:
```python
def process_chat(message):
    # Everything in one function
    if "add" in message or "create" in message:
        title = extract_title(message)
        priority = extract_priority(message)
        task = create_task(title, priority)
        return f"Created {task.title}"
    elif "show" in message:
        tasks = get_tasks()
        return format_tasks(tasks)
    # ...hundreds of lines...
```

**After (Agent-Based)**:
```python
def process_chat(message):
    service = ChatbotService()
    return service.process_message(db, user_id, message)
```

**Benefits**:
- ✅ Testable components
- ✅ Reusable across interfaces
- ✅ Easy to extend
- ✅ Clear separation of concerns

---

## Conclusion

**Reusable Intelligence** in AI TaskMaster is achieved through:

1. **Modular Agent Design**: Each agent is an independent, reusable component
2. **Clear Interfaces**: Well-defined contracts between agents
3. **Composition over Inheritance**: Agents are composed, not tightly coupled
4. **Dependency Injection**: Easy to swap implementations
5. **Stateless Architecture**: Agents don't maintain internal state
6. **Cross-Platform Portability**: Same agents work in web, CLI, mobile, voice
7. **Extensibility**: Easy to add capabilities without breaking existing code
8. **Testability**: Each component can be tested in isolation

This architecture enables the same AI intelligence to be reused across:
- Different user interfaces (web, mobile, voice)
- Different platforms (cloud, on-premise, edge)
- Different languages (English, Urdu, Spanish)
- Different AI providers (Gemini, OpenAI, Anthropic)
- Different use cases (todo, notes, calendar, CRM)

**The result**: A truly reusable AI system that maximizes code reuse while minimizing coupling and maximizing flexibility.
