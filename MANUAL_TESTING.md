# Manual Testing Checklist

**Feature**: 002-fullstack-web-auth
**Last Updated**: 2025-12-31
**Testing Environment**: http://localhost:3001 (frontend), http://localhost:8000 (backend)

This checklist provides step-by-step manual testing procedures for the Todo Application frontend.

---

## Prerequisites

Before starting manual testing:

- [ ] Backend server is running: http://localhost:8000
- [ ] Frontend server is running: http://localhost:3001 (or 3000)
- [ ] Browser DevTools console is open (check for errors)
- [ ] Browser Network tab is open (monitor API requests)

---

## 1. Signup Flow

### Test Case 1.1: Successful Signup

**Steps**:
1. Navigate to http://localhost:3001
2. Click "Sign Up" link
3. Fill in the form:
   - Email: `test1@example.com`
   - Name: `Test User 1`
   - Password: `TestPass123`
4. Observe real-time password validation feedback:
   - [ ] Checkmarks appear as requirements are met
   - [ ] At least 8 characters ✓
   - [ ] One uppercase letter ✓
   - [ ] One lowercase letter ✓
   - [ ] One number ✓
5. Click "Create Account" button

**Expected Result**:
- [ ] "Account created" toast notification appears
- [ ] Automatically redirected to `/dashboard`
- [ ] Header shows user name: "Test User 1"
- [ ] Dashboard shows empty state: "No tasks yet. Create one above to get started!"

### Test Case 1.2: Signup with Existing Email

**Steps**:
1. Navigate to http://localhost:3001/signup
2. Fill in form with same email as Test 1.1
3. Click "Create Account"

**Expected Result**:
- [ ] Error toast appears: "Email already registered"
- [ ] Form remains on signup page
- [ ] No redirect occurs

### Test Case 1.3: Signup with Invalid Password

**Steps**:
1. Navigate to http://localhost:3001/signup
2. Fill in form with password: `short` (too short)
3. Observe validation feedback

**Expected Result**:
- [ ] Password validation shows unmet requirements (red X icons)
- [ ] "Create Account" button remains enabled (browser validation will catch it)

---

## 2. Login Flow

### Test Case 2.1: Successful Login

**Steps**:
1. Navigate to http://localhost:3001
2. Click "Log in" (if on signup page) or stay on login page
3. Fill in credentials:
   - Email: `test1@example.com`
   - Password: `TestPass123`
4. Click "Log in" button

**Expected Result**:
- [ ] "Login successful" toast appears
- [ ] Redirected to `/dashboard`
- [ ] User name appears in header

### Test Case 2.2: Login with Invalid Credentials

**Steps**:
1. Navigate to http://localhost:3001/login
2. Fill in credentials:
   - Email: `test1@example.com`
   - Password: `WrongPassword123`
3. Click "Log in" button

**Expected Result**:
- [ ] Error toast appears: "Invalid email or password"
- [ ] Form remains on login page
- [ ] No redirect occurs

### Test Case 2.3: Login with Non-Existent Email

**Steps**:
1. Fill in credentials:
   - Email: `nonexistent@example.com`
   - Password: `TestPass123`
2. Click "Log in" button

**Expected Result**:
- [ ] Error toast appears: "Invalid email or password" (same message for security)
- [ ] No redirect occurs

---

## 3. Task Management

### Test Case 3.1: Create Task

**Steps**:
1. Login as `test1@example.com`
2. Click "Add Task" button in dashboard
3. Dialog opens
4. Fill in form:
   - Title: `Buy groceries`
   - Description: `Milk, eggs, bread`
5. Click "Create Task" button

**Expected Result**:
- [ ] "Task created" toast appears
- [ ] Dialog closes
- [ ] New task appears in task list
- [ ] Task shows title: "Buy groceries"
- [ ] Task shows description: "Milk, eggs, bread"
- [ ] Task is unchecked (not completed)

### Test Case 3.2: Create Task with Keyboard (Accessibility)

**Steps**:
1. Click "Add Task" button
2. Press `Tab` to navigate to title input (should auto-focus)
3. Type title: `Keyboard test task`
4. Press `Enter` key

**Expected Result**:
- [ ] Form submits (same as clicking "Create Task")
- [ ] Task is created successfully

### Test Case 3.3: Cancel Task Creation with Escape Key

**Steps**:
1. Click "Add Task" button
2. Type some text in title field
3. Press `Escape` key

**Expected Result**:
- [ ] Dialog closes
- [ ] Task is NOT created
- [ ] No toast notification

### Test Case 3.4: Edit Task

**Steps**:
1. Find the task "Buy groceries"
2. Click "Edit" button
3. Modify:
   - Title: `Buy groceries and snacks`
   - Description: `Milk, eggs, bread, chips`
4. Click "Save" button

**Expected Result**:
- [ ] "Task updated" toast appears
- [ ] Edit mode exits
- [ ] Task shows updated title
- [ ] Task shows updated description

### Test Case 3.5: Cancel Task Edit

**Steps**:
1. Click "Edit" button on a task
2. Modify the title
3. Click "Cancel" button

**Expected Result**:
- [ ] Edit mode exits
- [ ] Original title/description restored
- [ ] No toast notification

### Test Case 3.6: Toggle Task Completion

**Steps**:
1. Find an uncompleted task
2. Click the checkbox

**Expected Result**:
- [ ] "Task updated" toast appears with "Task marked as complete"
- [ ] Task checkbox is checked
- [ ] Task title has line-through styling
- [ ] Task description has line-through styling
- [ ] Task background changes to gray (bg-gray-50)

### Test Case 3.7: Toggle Task Back to Incomplete

**Steps**:
1. Find a completed task (from Test 3.6)
2. Click the checkbox again

**Expected Result**:
- [ ] "Task updated" toast appears with "Task marked as incomplete"
- [ ] Task checkbox is unchecked
- [ ] Line-through styling removed
- [ ] Task background returns to white

### Test Case 3.8: Delete Task

**Steps**:
1. Click "Delete" button on a task
2. Confirmation modal appears
3. Click "Delete" button in modal

**Expected Result**:
- [ ] "Task deleted" toast appears
- [ ] Modal closes
- [ ] Task is removed from list

### Test Case 3.9: Cancel Task Deletion

**Steps**:
1. Click "Delete" button on a task
2. Confirmation modal appears
3. Click "Cancel" button

**Expected Result**:
- [ ] Modal closes
- [ ] Task remains in list
- [ ] No toast notification

### Test Case 3.10: Delete with Keyboard (Accessibility)

**Steps**:
1. Click "Delete" button
2. Modal opens
3. Press `Enter` key

**Expected Result**:
- [ ] Task is deleted (Enter confirms in modal)

---

## 4. Logout and Session Management

### Test Case 4.1: Logout

**Steps**:
1. While logged in, click "Logout" button in header
2. Wait for redirect

**Expected Result**:
- [ ] Redirected to `/login`
- [ ] No longer see dashboard content
- [ ] Cannot navigate to `/dashboard` (should redirect back to login)

### Test Case 4.2: Task Persistence After Logout

**Steps**:
1. Create a task (e.g., "Persistence test")
2. Logout
3. Login again with same credentials
4. Navigate to `/dashboard`

**Expected Result**:
- [ ] Previously created task is still present
- [ ] Task data is unchanged (title, description, completion status)

---

## 5. Responsive Design (Mobile)

### Test Case 5.1: Mobile Signup

**Steps**:
1. Open DevTools and set device emulation to iPhone 12
2. Navigate to signup page
3. Complete signup flow

**Expected Result**:
- [ ] Form stacks vertically on small screen
- [ ] Buttons are touch-friendly (>= 44px × 44px)
- [ ] Password validation checklist readable
- [ ] No horizontal scrolling required

### Test Case 5.2: Mobile Dashboard

**Steps**:
1. Login on mobile viewport
2. View task list

**Expected Result**:
- [ ] Header stacks (user name hidden on mobile, only logout button visible)
- [ ] Task grid shows 1 column (grid-cols-1)
- [ ] "Add Task" button spans full width
- [ ] Checkboxes are >= 44px × 44px
- [ ] "Edit" and "Delete" buttons are >= 44px × 44px

### Test Case 5.3: Tablet Dashboard

**Steps**:
1. Set viewport to iPad (768px)
2. View task list

**Expected Result**:
- [ ] Task grid shows 2 columns (md:grid-cols-2)
- [ ] Header shows user name and logout button side-by-side

### Test Case 5.4: Desktop Dashboard

**Steps**:
1. Set viewport to desktop (1024px+)
2. View task list

**Expected Result**:
- [ ] Task grid shows 3 columns (lg:grid-cols-3)

---

## 6. Error Handling

### Test Case 6.1: Network Error (Backend Down)

**Steps**:
1. Stop backend server
2. Attempt to login

**Expected Result**:
- [ ] Error toast appears: "Unable to connect to server. Please check your connection and try again."
- [ ] No crash or blank page
- [ ] User can retry after restarting backend

### Test Case 6.2: JWT Token Expiration

**Note**: Access tokens expire after 15 minutes.

**Steps**:
1. Login
2. Wait 16 minutes (or modify access token expiry in code temporarily to 1 minute for faster testing)
3. Try to create a task

**Expected Result**:
- [ ] "Session expired. Please log in again." toast appears
- [ ] Automatically redirected to `/login?redirect=/dashboard`
- [ ] After re-login, redirected back to dashboard

---

## 7. Accessibility

### Test Case 7.1: Keyboard Navigation

**Steps**:
1. Navigate site using only keyboard (Tab, Enter, Escape)
2. Complete signup, login, and task management

**Expected Result**:
- [ ] All interactive elements reachable via Tab
- [ ] Enter key submits forms
- [ ] Escape key closes dialogs
- [ ] Focus indicators visible on all elements

### Test Case 7.2: Screen Reader (Optional)

**Steps**:
1. Enable screen reader (NVDA/JAWS on Windows, VoiceOver on Mac)
2. Navigate site

**Expected Result**:
- [ ] ARIA labels announced correctly
- [ ] Form fields have descriptive labels
- [ ] Buttons have clear purposes announced
- [ ] Task completion status announced

---

## 8. Browser Compatibility

### Test Case 8.1: Chrome

- [ ] All features work in Google Chrome (latest)

### Test Case 8.2: Firefox

- [ ] All features work in Mozilla Firefox (latest)

### Test Case 8.3: Safari

- [ ] All features work in Safari (latest, macOS/iOS)

### Test Case 8.4: Edge

- [ ] All features work in Microsoft Edge (latest)

---

## 9. Performance

### Test Case 9.1: Page Load Time

**Steps**:
1. Open DevTools Network tab
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Measure total load time

**Expected Result**:
- [ ] Initial load < 3 seconds on fast 3G
- [ ] No blocking resources

### Test Case 9.2: API Response Time

**Steps**:
1. Monitor Network tab during task operations
2. Check response times for API calls

**Expected Result**:
- [ ] GET /api/tasks < 200ms
- [ ] POST /api/tasks < 200ms
- [ ] PUT /api/tasks/{id} < 200ms
- [ ] DELETE /api/tasks/{id} < 200ms
- [ ] PATCH /api/tasks/{id}/toggle < 200ms

---

## 10. Edge Cases

### Test Case 10.1: Empty Task Title

**Steps**:
1. Click "Add Task"
2. Leave title empty
3. Click "Create Task"

**Expected Result**:
- [ ] Browser validation prevents submission (HTML5 `required` attribute)
- [ ] Toast appears: "Title cannot be empty" (if backend validates)

### Test Case 10.2: Maximum Title Length

**Steps**:
1. Create task with title of 200 characters
2. Try to type more

**Expected Result**:
- [ ] Input stops at 200 characters (`maxLength={200}`)
- [ ] Character counter shows "200/200"

### Test Case 10.3: Maximum Description Length

**Steps**:
1. Create task with description of 2000 characters
2. Try to type more

**Expected Result**:
- [ ] Input stops at 2000 characters (`maxLength={2000}`)
- [ ] Character counter shows "2000/2000"

---

## Test Summary

| Category | Passed | Failed | Notes |
|----------|--------|--------|-------|
| Signup Flow | /3 | /3 | |
| Login Flow | /3 | /3 | |
| Task Management | /10 | /10 | |
| Logout & Sessions | /2 | /2 | |
| Responsive Design | /4 | /4 | |
| Error Handling | /2 | /2 | |
| Accessibility | /2 | /2 | |
| Browser Compat | /4 | /4 | |
| Performance | /2 | /2 | |
| Edge Cases | /3 | /3 | |
| **Total** | **/35** | **/35** | |

---

## Tester Sign-Off

**Tested By**: _______________
**Test Date**: _______________
**Environment**: http://localhost:3001
**Result**: ☐ All tests passed ☐ Some tests failed
**Notes**: _______________
