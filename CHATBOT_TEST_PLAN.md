# AI Chatbot Test Plan - Comprehensive Validation

## Test Environment
- Backend: http://localhost:8000
- Frontend: http://localhost:3001
- Test User: Will be created during tests

## Test Categories

### 1. Natural Language Commands (Deliverable Requirement)

#### Test Scenario 1.1: Basic Task Creation
| User Says | Expected Intent | Expected Tool Call | Expected Entities |
|-----------|----------------|-------------------|-------------------|
| "Add a task to buy groceries" | create_task | add_task | title: "buy groceries" |
| "I need to remember to pay bills" | create_task | add_task | title: "pay bills" |
| "Remind me to call mom tomorrow" | create_task | add_task | title: "call mom", due_date: tomorrow |

#### Test Scenario 1.2: Task Listing
| User Says | Expected Intent | Expected Tool Call | Expected Filter |
|-----------|----------------|-------------------|-----------------|
| "Show me all my tasks" | list_tasks | list_tasks | status: "all" |
| "What's pending?" | list_tasks | list_tasks | status: "pending" |
| "What have I completed?" | list_tasks | list_tasks | status: "completed" |
| "List my tasks" | list_tasks | list_tasks | status: "all" |

#### Test Scenario 1.3: Task Completion
| User Says | Expected Intent | Expected Tool Call | Expected Task ID |
|-----------|----------------|-------------------|------------------|
| "Mark task 3 as complete" | complete_task | complete_task | task_id: 3 |
| "Complete task 5" | complete_task | complete_task | task_id: 5 |
| "Done with task 2" | complete_task | complete_task | task_id: 2 |

#### Test Scenario 1.4: Task Deletion by ID
| User Says | Expected Intent | Expected Tool Call | Expected Task ID |
|-----------|----------------|-------------------|------------------|
| "Delete task 4" | delete_task | delete_task | task_id: 4 |
| "Remove task 1" | delete_task | delete_task | task_id: 1 |
| "Delete id 20" | delete_task | delete_task | task_id: 20 |

#### Test Scenario 1.5: Task Update
| User Says | Expected Intent | Expected Tool Call | Expected Data |
|-----------|----------------|-------------------|---------------|
| "Change task 1 to 'Call mom tonight'" | update_task | update_task | task_id: 1, title: "Call mom tonight" |
| "Update task 3 to buy milk" | update_task | update_task | task_id: 3, title: "buy milk" |

---

### 2. Memory Persistence (10+ Message History)

#### Test Scenario 2.1: Context Retention
```
Conversation Flow:
1. User: "Add a task to buy groceries"
2. Bot: "✓ Created task..."
3. User: "Add another one for gym"
4. Bot: Should understand "another one" = another task
5. Continue for 10+ messages
6. User: "Show my tasks"
7. Bot: Should list ALL tasks from this conversation
```

**Expected**: Bot maintains context across 10+ messages

#### Test Scenario 2.2: Reference Previous Tasks
```
1. User: "Create task go to gym"
2. Bot: "✓ Created..."
3. User: "Create task test the bot"
4. Bot: "✓ Created..."
...10 more messages...
15. User: "Mark that gym task as done"
16. Bot: Should find "go to gym" task from message #1
```

---

### 3. Task Recognition WITHOUT Exact Match (Critical Requirement)

#### Test Scenario 3.1: The "go to gym" Problem
```
Setup:
- Task exists: "go to gym" (ID: 30)

User Input | Expected Behavior | Why It Should Work
-----------|-------------------|-------------------
"delete task go to gym" | Find task 30 | Exact match
"delete task go gym" | Find task 30 | Partial match (missing "to")
"remove gym task" | Find task 30 | Keyword match
"delete the gym one" | Find task 30 | Fuzzy reference
```

**CRITICAL**: System MUST NOT fail with "No tasks found matching 'go  gym'" (double space issue)

#### Test Scenario 3.2: The "test the bot" Problem
```
Setup:
- Task exists: "test the bot" (ID: 19)

User Input | Expected Behavior | Issue
-----------|-------------------|-------
"mark test the bot as completed" | Find task 19 | Must preserve "the"
"complete test bot" | Find task 19 | Partial match
"mark that test task done" | Find task 19 | Fuzzy match
```

**CRITICAL**: System MUST NOT strip "the" from "test the bot" per intent_classifier.py:133

#### Test Scenario 3.3: Task Reference by Number
```
Setup:
- Task 1: "Do chat page update"
- Task 2: "go to gym"
- Task 3: "jhf"
- Task 4: "test the bot"

User Input | Expected Behavior
-----------|------------------
"remove task4" | Delete task 4 (no space)
"delete task 4" | Delete task 4 (with space)
"complete #3" | Mark task 3 complete
"mark task number 2 done" | Mark task 2 complete
```

---

### 4. Intent Understanding WITHOUT Keywords

#### Test Scenario 4.1: Implicit Intent Recognition
| User Says (No Keywords) | Expected Intent | Reasoning |
|------------------------|----------------|-----------|
| "What's my pending tasks?" | list_tasks | Implied "show"/"list" |
| "Buy milk tomorrow" | create_task | Implied "add"/"create" |
| "Call mom tonight" | create_task | Implied task creation |
| "Finished with the groceries" | complete_task | Implied completion |
| "Get rid of task 5" | delete_task | Implied deletion |

#### Test Scenario 4.2: Conversational Commands
| User Says | Expected Intent | Expected Action |
|-----------|----------------|-----------------|
| "I need to call mom" | create_task | Create task "call mom" |
| "Don't forget to buy milk" | create_task | Create task "buy milk" |
| "I'm done with the gym" | Need clarification | Which gym task? |

---

### 5. Typo Tolerance & Fuzzy Matching

#### Test Scenario 5.1: Typos in Commands
| User Input (Typos) | Expected Classification | Expected Tool |
|-------------------|------------------------|---------------|
| "shw my tsks" | list_tasks | list_tasks |
| "ad tsk buy milk" | create_task | add_task |
| "dlete teh first one" | delete_task | delete_task |
| "mkr tsk 5 complet" | complete_task | complete_task |

#### Test Scenario 5.2: Typos in Task Titles
```
Setup:
- Task: "test the bot"

User Input | Expected Behavior
-----------|------------------
"delete test teh bot" | Should find "test the bot"
"mark tst the bt done" | Should suggest matches
```

---

### 6. Conversation Flow (Stateless + History)

#### Test Scenario 6.1: New Conversation
```
Request 1:
POST /api/chat
{
  "message": "Add task buy groceries",
  "conversation_id": null
}

Expected:
- conversation_id returned (new UUID)
- User message saved to DB
- Assistant response saved to DB
- Server state: EMPTY (stateless)
```

#### Test Scenario 6.2: Continuation
```
Request 2:
POST /api/chat
{
  "message": "Show my tasks",
  "conversation_id": "<uuid-from-request-1>"
}

Expected:
- Same conversation_id used
- History loaded (Request 1 messages)
- Context available for classification
- Response includes tasks from Request 1
- Server state: STILL EMPTY (stateless)
```

#### Test Scenario 6.3: Long Conversation (10+ Messages)
```
1. Create task 1
2. Create task 2
3. List tasks
4. Create task 3
5. Mark task 1 done
6. Create task 4
7. Update task 2
8. List tasks
9. Delete task 3
10. Create task 5
11. Show completed tasks
12. User: "Mark that first one done"
    Expected: Bot should reference task from message history
```

---

### 7. Edge Cases

#### Test Scenario 7.1: Ambiguous References
```
Setup:
- Task 1: "Buy milk"
- Task 2: "Buy groceries"

User: "Delete the buy task"
Expected: "Which one? You have 2 tasks with 'buy'..."
```

#### Test Scenario 7.2: Non-Existent Tasks
```
User: "Delete task 999"
Expected: "Task not found"

User: "Mark task 'xyz' done"
Expected: "No task found matching 'xyz'"
```

#### Test Scenario 7.3: Empty/Unclear Input
```
User: "hey"
Expected: Unclear intent, helpful message

User: "h"
Expected: Unclear intent, helpful message

User: "add new task"
Expected: "What task would you like to add?"
```

---

## Test Execution Strategy

### Phase 1: Manual Browser Testing
1. Login to http://localhost:3001
2. Navigate to Chat page
3. Execute each test scenario
4. Document results

### Phase 2: API Testing (curl/Postman)
1. Get JWT token
2. Test `/api/chat` endpoint directly
3. Verify conversation persistence
4. Check database state

### Phase 3: Critical Issue Verification
1. **The "go to gym" bug** - MUST fix
2. **The "test the bot" bug** - MUST fix
3. **Task reference without exact match** - MUST work
4. **Memory across 10+ messages** - MUST work

---

## Success Criteria

### Must Pass (Critical):
- [ ] All 8 deliverable commands work
- [ ] Memory persists across 10+ messages
- [ ] Task recognition WITHOUT exact match
- [ ] Intent understanding WITHOUT keywords
- [ ] Typo tolerance for common mistakes
- [ ] Stateless server with history from DB

### Should Pass (Important):
- [ ] Fuzzy task matching
- [ ] Ambiguity handling
- [ ] Graceful error messages

### Nice to Have:
- [ ] Context-aware pronouns ("it", "that")
- [ ] Multi-task operations

---

## Known Issues to Verify

From user report:
1. ❌ "delete task go to gym" → "No tasks found matching 'go  gym'" (double space?)
2. ❌ "show my tasks" works but shows tasks
3. ❌ "remove task4" → "I couldn't find that task"
4. ❌ "remove test the bot" → "No tasks found matching 'test  bot'" (strips "the"?)

**These MUST be tested and results documented.**
