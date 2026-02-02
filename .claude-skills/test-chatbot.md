# Test Chatbot - AI Agent Testing Automation Skill

## Description
Automated testing skill for AI TaskMaster chatbot. Validates natural language understanding, intent classification, task resolution, and end-to-end conversation flows.

## Usage
```
/test-chatbot [suite] [--verbose] [--coverage]
```

**Parameters:**
- `suite`: Test suite to run (unit|integration|e2e|all)
- `--verbose`: Show detailed test output
- `--coverage`: Generate coverage report

**Examples:**
```bash
/test-chatbot unit                    # Run unit tests for all agents
/test-chatbot integration             # Run integration tests
/test-chatbot e2e                     # Run end-to-end conversation tests
/test-chatbot all --coverage          # Run all tests with coverage report
```

## Test Suites

### 1. Unit Tests - Agent Isolation

Test each agent independently with mocked dependencies.

**IntentClassifierAgent Tests:**
```python
def test_create_task_intent():
    """Test intent classification for task creation."""
    agent = IntentClassifierAgent()

    test_cases = [
        ("remind me to buy milk", "create_task"),
        ("add a task to call mom", "create_task"),
        ("I need to remember to pay bills", "create_task"),
        ("Buy groceries tomorrow", "create_task"),
    ]

    for message, expected_intent in test_cases:
        result = agent.classify(message)
        assert result["intent"] == expected_intent
        assert result["confidence"] > 0.7

def test_typo_tolerance():
    """Test typo normalization in classifier."""
    agent = IntentClassifierAgent()

    # "shw my tsks" should still work
    result = agent.classify("shw my tsks")
    assert result["intent"] == "list_tasks"

def test_entity_extraction():
    """Test entity extraction from messages."""
    agent = IntentClassifierAgent()

    result = agent.classify("add a high priority task to buy milk tomorrow")
    assert result["entities"]["title"] == "buy milk"
    assert result["entities"]["priority"] == "high"
    assert "due_date" in result["entities"]
```

**TaskResolutionAgent Tests:**
```python
def test_fuzzy_task_matching():
    """Test word-overlap fuzzy matching."""
    agent = TaskResolutionAgent()

    # Setup: Create test tasks
    tasks = [
        {"id": 1, "title": "Buy groceries at store"},
        {"id": 2, "title": "Call mom tomorrow"},
        {"id": 3, "title": "Grocery shopping list"}
    ]

    # Test: "grocery" should match tasks 1 and 3
    result = agent.resolve(db, "user-123", {"task_reference": "grocery"})
    assert 1 in result["task_ids"]
    assert 3 in result["task_ids"]

def test_explicit_id_resolution():
    """Test direct task ID resolution."""
    agent = TaskResolutionAgent()

    result = agent.resolve(db, "user-123", {"task_id": 5})
    assert result["task_ids"] == [5]
    assert not result["confirmation_needed"]
```

**ActionAgent Tests:**
```python
def test_create_task_action():
    """Test MCP tool execution for task creation."""
    agent = ActionAgent()

    result = agent.execute(
        db=test_db,
        intent="create_task",
        parameters={"title": "Test task", "priority": "high"},
        user_id="user-123"
    )

    assert result["success"] is True
    assert result["task"]["title"] == "Test task"
    assert result["task"]["priority"] == "high"

def test_user_isolation():
    """Test that users only access their own tasks."""
    agent = ActionAgent()

    # User A creates task
    result_a = agent.execute(db, "create_task", {"title": "Task A"}, "user-a")
    task_id = result_a["task"]["id"]

    # User B tries to access User A's task
    result_b = agent.execute(db, "delete_task", {"task_id": task_id}, "user-b")
    assert result_b["success"] is False
    assert "not found" in result_b["error"].lower()
```

**ResponseFormatterAgent Tests:**
```python
def test_create_task_response():
    """Test natural language response formatting."""
    agent = ResponseFormatterAgent()

    result = agent.format_response(
        intent="create_task",
        result={"success": True, "task": {"id": 5, "title": "Buy milk"}}
    )

    assert "Buy milk" in result["response"]
    assert "5" in result["response"]  # Task ID mentioned
    assert result["response"].startswith("✓")  # Success indicator

def test_error_response():
    """Test error message formatting."""
    agent = ResponseFormatterAgent()

    result = agent.format_response(
        intent="delete_task",
        result={"success": False, "error": "Task not found"}
    )

    assert "couldn't find" in result["response"].lower()
    assert "helpful" in result["response"].lower() or "try" in result["response"].lower()
```

### 2. Integration Tests - Agent Pipeline

Test agents working together in realistic scenarios.

```python
def test_create_and_list_flow():
    """Test full conversation: create task then list tasks."""
    service = ChatbotService()

    # Create task
    response1 = service.process_message(
        db=test_db,
        user_id="user-123",
        message="remind me to buy milk"
    )
    assert response1["intent"] == "create_task"
    assert "buy milk" in response1["response"].lower()

    # List tasks
    response2 = service.process_message(
        db=test_db,
        user_id="user-123",
        message="show my tasks"
    )
    assert response2["intent"] == "list_tasks"
    assert "buy milk" in response2["response"].lower()

def test_update_task_flow():
    """Test updating a task via natural language."""
    service = ChatbotService()

    # Create task
    response1 = service.process_message(db, "user-123", "add task buy milk")

    # Extract task ID from response (assuming format "ID: 5")
    import re
    match = re.search(r'ID: (\d+)', response1["response"])
    task_id = match.group(1)

    # Update task
    response2 = service.process_message(
        db, "user-123", f"update id {task_id} to high priority"
    )
    assert response2["intent"] == "update_task"
    assert "high" in response2["response"].lower()

def test_conversation_context():
    """Test conversation history is maintained."""
    service = ChatbotService()

    # First message creates conversation
    response1 = service.process_message(db, "user-123", "create task test")
    conversation_id = response1["conversation_id"]

    # Second message uses same conversation
    response2 = service.process_message(
        db, "user-123", "mark it as complete",
        conversation_id=conversation_id
    )

    # "it" should refer to the task from previous message
    assert response2["success"] is True
```

### 3. End-to-End Tests - User Scenarios

Test complete user workflows from login to task management.

```python
def test_new_user_onboarding():
    """Test new user signup and first task creation."""
    # 1. User signs up
    auth_response = client.post("/api/auth/signup", json={
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "name": "New User"
    })
    assert auth_response.status_code == 201
    token = auth_response.json()["access_token"]

    # 2. User creates first task via chat
    chat_response = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"message": "remind me to set up my profile"}
    )
    assert chat_response.status_code == 200
    assert "set up my profile" in chat_response.json()["response"].lower()

def test_natural_language_variations():
    """Test different phrasings for same intent."""
    service = ChatbotService()

    variations = [
        "show my tasks",
        "what are my tasks",
        "list all tasks",
        "what do I need to do",
        "show pending items"
    ]

    for message in variations:
        response = service.process_message(db, "user-123", message)
        assert response["intent"] == "list_tasks"
        assert response["success"] is True

def test_error_handling_gracefully():
    """Test graceful error handling for edge cases."""
    service = ChatbotService()

    # Try to delete non-existent task
    response = service.process_message(db, "user-123", "delete task 99999")
    assert "couldn't find" in response["response"].lower()
    assert response["success"] is False

    # Try with unclear intent
    response = service.process_message(db, "user-123", "hello")
    assert response["intent"] == "unclear"
```

## Test Execution Commands

### Run All Tests
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=src/agents --cov=src/services/chatbot_service

# Expected output:
# tests/test_intent_classifier.py::test_create_task_intent PASSED
# tests/test_task_resolution.py::test_fuzzy_matching PASSED
# tests/test_action_agent.py::test_user_isolation PASSED
# Coverage: 85%
```

### Run Specific Test Files
```bash
# Intent classifier tests only
pytest tests/test_intent_classifier.py -v

# Integration tests only
pytest tests/test_conversation_flow.py -v

# With detailed output
pytest tests/ -vv --tb=short
```

### Generate Coverage Report
```bash
pytest tests/ --cov=src/agents --cov=src/services --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## Manual Testing Scenarios

### Scenario 1: Natural Language Understanding
```
User: "Buy milk"
Expected: Creates task "Buy milk"
Status: ✅ PASS

User: "I need to remember to call mom tomorrow"
Expected: Creates task "call mom" with due date
Status: ✅ PASS

User: "shw my tsks"  # Typos
Expected: Lists tasks (typo-tolerant)
Status: ✅ PASS
```

### Scenario 2: Fuzzy Task Matching
```
User: "create task Buy groceries at Whole Foods"
Bot: "✓ Created task: 'Buy groceries at Whole Foods' (ID: 5)"

User: "mark grocery as done"  # Partial reference
Expected: Completes task ID 5
Status: ✅ PASS

User: "delete the grocery one"  # Natural reference
Expected: Deletes task ID 5
Status: ✅ PASS
```

### Scenario 3: Priority and Metadata
```
User: "add a high priority task to fix bug"
Expected: Creates task with priority="high"
Status: ✅ PASS

User: "update task 5 to medium priority"
Expected: Updates task 5 priority
Status: ✅ PASS
```

## Performance Tests

### Response Time SLA
```python
def test_chat_response_time():
    """Ensure chat endpoint meets <5s p95 latency SLA."""
    import time

    service = ChatbotService()
    latencies = []

    for i in range(100):
        start = time.time()
        service.process_message(db, "user-123", "show my tasks")
        latency = time.time() - start
        latencies.append(latency)

    p95 = sorted(latencies)[94]  # 95th percentile
    assert p95 < 5.0, f"p95 latency {p95:.2f}s exceeds 5s SLA"
```

### Load Testing
```bash
# Using locust
locust -f tests/load_test.py --host=http://localhost:8000

# Test configuration:
# - 100 concurrent users
# - 10 requests per second
# - Duration: 5 minutes

# Expected performance:
# - p95 latency < 5s
# - Error rate < 1%
# - Throughput > 500 req/min
```

## Test Data Setup

### Create Test Fixtures
```python
@pytest.fixture
def test_db():
    """Create test database with sample data."""
    engine = create_engine("sqlite:///:memory:")
    with Session(engine) as session:
        # Create test user
        user = User(email="test@example.com", password_hash="...")
        session.add(user)

        # Create test tasks
        tasks = [
            Task(user_id=user.id, title="Buy milk", priority="high"),
            Task(user_id=user.id, title="Call mom", priority="medium"),
            Task(user_id=user.id, title="Pay bills", priority="low"),
        ]
        session.add_all(tasks)
        session.commit()

        yield session

@pytest.fixture
def mock_gemini():
    """Mock Gemini API for deterministic testing."""
    with patch('google.generativeai.GenerativeModel') as mock:
        mock.return_value.generate_content.return_value.text = json.dumps({
            "intent": "create_task",
            "confidence": 0.95,
            "entities": {"title": "test task"}
        })
        yield mock
```

## Success Criteria

Tests pass when:

✅ **Unit Tests**
- All agent tests passing (100% pass rate)
- Code coverage > 80% for agents
- No flaky tests (3 consecutive runs pass)

✅ **Integration Tests**
- All conversation flows working
- Agent pipeline functioning correctly
- Database operations successful

✅ **E2E Tests**
- All user scenarios passing
- Natural language variations handled
- Error cases graceful

✅ **Performance Tests**
- p95 latency < 5s
- No memory leaks
- Database connection pool healthy

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Chatbot Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: pytest backend/tests/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests Failing
```bash
# Check test database
pytest tests/ -v --tb=short  # Show short traceback

# Run single failing test
pytest tests/test_intent_classifier.py::test_create_task_intent -vv

# Check for race conditions
pytest tests/ --count=10  # Run 10 times
```

### Coverage Too Low
```bash
# Identify uncovered lines
pytest --cov=src/agents --cov-report=term-missing

# Focus on critical paths
pytest --cov=src/agents --cov-report=html
open htmlcov/index.html
```

## Related Documentation

- [Agent Architecture](../docs/agents-architecture.md)
- [Reusable Intelligence](../docs/reusable-intelligence.md)
- [API Documentation](http://localhost:8000/docs)

## Skill Metadata

- **Type**: Testing
- **Category**: QA, Automation
- **Complexity**: Medium
- **Requires**: pytest, coverage
- **Estimated Duration**: 2-5 minutes per suite
- **Coverage Target**: >80% for agents
