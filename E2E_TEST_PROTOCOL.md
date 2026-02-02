# End-to-End Test Protocol - Production Readiness Validation

**Project**: AI TaskMaster
**Test Date**: 2026-02-01
**Tester**: Production Engineering Team
**Objective**: Validate complete user flows before Vercel deployment

---

## Test Environment Setup

### Prerequisites
- [ ] Backend running: `cd backend && uvicorn src.main:app --reload`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Database: Neon PostgreSQL (production)
- [ ] Browser: Chrome/Edge (latest)
- [ ] Browser console: Open (F12) for error monitoring

### Environment URLs
- Backend: http://localhost:8000
- Frontend: http://localhost:3000 (or auto-selected port)
- API Docs: http://localhost:8000/docs

---

## E2E Test Suite

### Test 1: User Registration & Authentication Flow

**Objective**: Validate complete auth workflow from signup to logout

#### 1.1 User Signup
- [ ] Navigate to http://localhost:3000
- [ ] Click "Sign Up" button
- [ ] Fill form:
  - Name: "E2E Test User"
  - Email: "e2e.test@example.com"
  - Password: "SecurePass123!"
  - Confirm Password: "SecurePass123!"
- [ ] Click "Sign Up"
- [ ] **Expected**: Redirect to dashboard
- [ ] **Expected**: Welcome message displayed
- [ ] **Verify**: Browser console has no errors
- [ ] **Verify**: JWT token stored in cookies (DevTools → Application → Cookies)

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 1.2 User Logout
- [ ] Click profile/logout button
- [ ] **Expected**: Redirect to login page
- [ ] **Expected**: JWT token removed from cookies
- [ ] **Expected**: Cannot access /dashboard directly (redirects to login)

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 1.3 User Login
- [ ] On login page, enter:
  - Email: "e2e.test@example.com"
  - Password: "SecurePass123!"
- [ ] Click "Login"
- [ ] **Expected**: Redirect to dashboard
- [ ] **Expected**: Tasks loaded (empty or populated)
- [ ] **Verify**: No console errors

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 1.4 Invalid Login Attempt
- [ ] Logout
- [ ] Attempt login with wrong password
- [ ] **Expected**: Error message displayed
- [ ] **Expected**: Not redirected
- [ ] **Expected**: Password field cleared

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 2: Task Management (UI)

**Objective**: Validate CRUD operations via traditional UI

#### 2.1 Create Task
- [ ] Login as test user
- [ ] Click "New Task" button (or press 'N' key)
- [ ] Fill form:
  - Title: "E2E Test Task 1"
  - Description: "Testing task creation"
  - Priority: High
  - Due Date: Tomorrow
  - Tags: "testing, e2e"
- [ ] Click "Create"
- [ ] **Expected**: Task appears in task list
- [ ] **Expected**: Success toast notification
- [ ] **Verify**: Task shows correct priority badge (red for high)
- [ ] **Verify**: Due date displays correctly

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 2.2 Read/List Tasks
- [ ] View task list
- [ ] **Expected**: Created task visible
- [ ] **Expected**: Task shows all details (title, description, priority, due date)
- [ ] Test filters:
  - [ ] Filter by priority (High)
  - [ ] Filter by status (Pending)
  - [ ] Search by title ("E2E Test")
- [ ] **Expected**: Filters work correctly

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 2.3 Update Task
- [ ] Click on task to edit
- [ ] Update:
  - Title: "E2E Test Task 1 (Updated)"
  - Priority: Medium
- [ ] Save changes
- [ ] **Expected**: Task updates immediately
- [ ] **Expected**: Priority badge changes to yellow/orange
- [ ] **Expected**: Success toast notification

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 2.4 Complete Task
- [ ] Click checkbox or "Mark Complete" button
- [ ] **Expected**: Task marked as completed
- [ ] **Expected**: Visual indicator (strikethrough or checkmark)
- [ ] **Expected**: Completion animation (if implemented)
- [ ] Toggle back to incomplete
- [ ] **Expected**: Task returns to pending state

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 2.5 Delete Task
- [ ] Click delete button on task
- [ ] **Expected**: Confirmation dialog appears
- [ ] Confirm deletion
- [ ] **Expected**: Task removed from list
- [ ] **Expected**: Success toast notification

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 3: AI Chatbot Interface (Phase III Critical)

**Objective**: Validate natural language task management via chatbot

#### 3.1 Create Task via Chat
- [ ] Navigate to chat interface
- [ ] Type: "add task buy groceries tomorrow"
- [ ] Send message
- [ ] **Expected**: AI response confirms task creation
- [ ] **Expected**: Task appears in task list
- [ ] **Expected**: Response time <5 seconds
- [ ] **Verify**: Task has correct title "buy groceries"
- [ ] **Verify**: Due date set to tomorrow

**Result**: ⬜ PASS / ⬜ FAIL
**Response Time**: _______ seconds
**Notes**: _____________________________________________

#### 3.2 List Tasks via Chat
- [ ] Type: "show my tasks"
- [ ] Send message
- [ ] **Expected**: AI lists all user tasks
- [ ] **Expected**: Response includes task details
- [ ] **Expected**: Only user's tasks shown (user isolation)

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 3.3 Complete Task via Chat
- [ ] Type: "mark task 1 as done" (or use task title)
- [ ] Send message
- [ ] **Expected**: AI confirms task completion
- [ ] **Expected**: Task marked complete in UI
- [ ] **Verify**: Task appears in "Completed" filter

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 3.4 Update Task via Chat
- [ ] Type: "update task 1 to call doctor"
- [ ] Send message
- [ ] **Expected**: AI confirms update
- [ ] **Expected**: Task title changed in UI

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 3.5 Delete Task via Chat
- [ ] Type: "delete the grocery task"
- [ ] Send message
- [ ] **Expected**: AI confirms deletion (or asks for confirmation)
- [ ] If confirmation required, confirm
- [ ] **Expected**: Task removed from list

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 3.6 Conversation Persistence
- [ ] Send multiple messages in chat
- [ ] Refresh page
- [ ] **Expected**: Chat history preserved
- [ ] **Expected**: Conversation continues with context

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 4: Voice Input (Phase III Feature)

**Objective**: Validate voice command functionality

#### 4.1 Voice Permission
- [ ] Click microphone button in chat
- [ ] **Expected**: Browser requests microphone permission
- [ ] Grant permission
- [ ] **Expected**: Recording indicator appears

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 4.2 Voice Command Execution
- [ ] Click microphone button
- [ ] Speak: "Add a task to prepare presentation"
- [ ] **Expected**: Speech transcribed to text
- [ ] **Expected**: Message auto-sent to chatbot
- [ ] **Expected**: Task created successfully

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 5: Multi-Language Support (Urdu)

**Objective**: Validate Urdu language toggle

#### 5.1 Language Toggle
- [ ] In chat interface, find language toggle
- [ ] Switch to Urdu (اردو)
- [ ] Send message: "show my tasks"
- [ ] **Expected**: Response in Urdu
- [ ] **Expected**: Proper Urdu typography/font rendering
- [ ] Switch back to English
- [ ] **Expected**: Response in English

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 6: User Isolation & Security

**Objective**: Validate users cannot access each other's data

#### 6.1 Create Second User
- [ ] Logout
- [ ] Sign up with different email: "e2e.test2@example.com"
- [ ] Login as User 2
- [ ] Create task: "User 2 Private Task"

**Result**: ⬜ PASS / ⬜ FAIL

#### 6.2 Verify Isolation
- [ ] Logout
- [ ] Login as User 1 (e2e.test@example.com)
- [ ] View task list
- [ ] **Expected**: User 2's task NOT visible
- [ ] **Expected**: Only User 1's tasks shown

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 6.3 Chat Isolation
- [ ] As User 1, ask chatbot: "show all tasks"
- [ ] **Expected**: Only User 1's tasks returned
- [ ] **Expected**: No access to User 2's data

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 7: Responsive Design & Mobile

**Objective**: Validate mobile/tablet responsiveness

#### 7.1 Mobile View (DevTools)
- [ ] Open DevTools (F12)
- [ ] Toggle device emulation (iPhone 14 Pro)
- [ ] **Expected**: Layout adapts to mobile
- [ ] **Expected**: Navigation collapses to hamburger menu
- [ ] **Expected**: Task cards stack vertically
- [ ] **Expected**: Touch targets ≥44px

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 7.2 Tablet View
- [ ] Set viewport to iPad dimensions
- [ ] **Expected**: Hybrid layout (between mobile/desktop)
- [ ] **Expected**: All features accessible

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 8: Error Handling & Edge Cases

**Objective**: Validate graceful degradation

#### 8.1 Network Failure Simulation
- [ ] Open DevTools → Network tab
- [ ] Set throttling to "Offline"
- [ ] Attempt to create task via chat
- [ ] **Expected**: Error message displayed
- [ ] **Expected**: No silent failure
- [ ] **Expected**: Retry option available

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 8.2 Invalid Chat Input
- [ ] Send gibberish to chatbot: "asdfjkl;asdfjkl;"
- [ ] **Expected**: AI responds gracefully (asks for clarification or suggests help)
- [ ] **Expected**: No crash or 500 error

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

#### 8.3 Empty Task Title
- [ ] Attempt to create task with empty title via UI
- [ ] **Expected**: Validation error displayed
- [ ] **Expected**: Submit button disabled or error toast

**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

### Test 9: Performance & Load

**Objective**: Validate acceptable performance under normal load

#### 9.1 Chat Response Time
- [ ] Send 5 consecutive chat messages
- [ ] Measure response time for each
- [ ] **Expected**: p95 latency <5 seconds
- [ ] **Expected**: No timeout errors

**Response Times**:
1. _______ seconds
2. _______ seconds
3. _______ seconds
4. _______ seconds
5. _______ seconds

**p95**: _______ seconds
**Result**: ⬜ PASS / ⬜ FAIL

#### 9.2 Task List Load Time
- [ ] Create 20 tasks via chat
- [ ] Refresh page
- [ ] Measure time to load task list
- [ ] **Expected**: <2 seconds for 20 tasks

**Load Time**: _______ seconds
**Result**: ⬜ PASS / ⬜ FAIL

---

### Test 10: Browser Console Errors

**Objective**: Validate zero critical errors in production build

#### 10.1 Console Audit
- [ ] Complete all above tests with console open
- [ ] Review all console messages
- [ ] **Expected**: No 404 errors
- [ ] **Expected**: No CORS errors
- [ ] **Expected**: No unhandled promise rejections
- [ ] **Acceptable**: Warnings only (non-blocking)

**Critical Errors Found**: _______
**Warnings Found**: _______
**Result**: ⬜ PASS / ⬜ FAIL
**Notes**: _____________________________________________

---

## Final Acceptance Criteria

### Critical (Must Pass - Deployment Blocker)
- [ ] User signup/login works without errors
- [ ] Tasks can be created via UI
- [ ] Tasks can be created via chatbot
- [ ] User isolation enforced (no cross-user data access)
- [ ] Zero critical console errors
- [ ] Chat response time <5 seconds (p95)
- [ ] Mobile responsive layout works

### Important (Should Pass - Document if Failed)
- [ ] Voice input works in supported browsers
- [ ] Urdu language toggle works
- [ ] All CRUD operations work via chat
- [ ] Task filters/search functional
- [ ] Error messages display correctly

### Nice to Have (Non-Blocking)
- [ ] Conversation history persists
- [ ] Animations smooth
- [ ] Toast notifications styled correctly

---

## Test Summary

**Total Tests Executed**: _______
**Passed**: _______
**Failed**: _______
**Pass Rate**: _______%

**Critical Failures**: _______
**Blocker Issues**: _______

---

## Go/No-Go Decision

**Deployment Recommendation**: ⬜ GO / ⬜ NO-GO

**Justification**: _______________________________________________

**Outstanding Issues**: _______________________________________________

**Sign-off**: _______________ (Tester) | Date: _______________
