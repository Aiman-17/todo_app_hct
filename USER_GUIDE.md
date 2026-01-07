# Todo Application - Advanced User Guide

This comprehensive guide covers all advanced features of the Todo Application, including search, filtering, keyboard shortcuts, animations, settings, and accessibility features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Task Management](#task-management)
3. [Search and Filtering](#search-and-filtering)
4. [Keyboard Navigation](#keyboard-navigation)
5. [Settings and Profile](#settings-and-profile)
6. [Animations and Visual Feedback](#animations-and-visual-feedback)
7. [Accessibility Features](#accessibility-features)
8. [Performance Optimizations](#performance-optimizations)
9. [Tips and Tricks](#tips-and-tricks)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Time Setup

1. **Sign Up**: Create an account with your name, email, and password
   - Password must be at least 8 characters
   - Real-time validation shows password strength
   - Passwords are hashed with bcrypt (12 rounds) for security

2. **Sign In**: Log in with your email and password
   - Sessions last 7 days (refresh token)
   - Access tokens refresh automatically every 15 minutes
   - Secure cookie-based authentication

3. **Dashboard**: After login, you'll see the main dashboard with:
   - Sidebar navigation (left)
   - Top navigation bar with your name
   - Command bar for search and filters
   - Task list (main content area)
   - Floating "+" button for quick task creation

---

## Task Management

### Creating Tasks

**Method 1: Floating Add Button**
- Click the orange "+" button in the bottom-right corner
- This button is always accessible on any page

**Method 2: Keyboard Shortcut**
- Press `N` anywhere in the app (except when typing in inputs)
- Fastest way for power users

**Task Form Fields:**
- **Title** (required): Short description of the task
- **Description** (optional): Additional details or notes
- **Priority** (optional): Low, Medium, or High
  - Color-coded indicators (blue, orange, red)
  - Affects task sorting
- **Due Date** (optional): Deadline for the task
  - Visual indicators for overdue tasks (red ring)
  - Relative date labels ("Today", "Tomorrow", "Next Week")
- **Tags** (optional): Categorize tasks with keywords
  - Displayed as pills on task cards
  - Searchable

### Viewing Tasks

**Task Card Layout:**
- **Checkbox** (left): Click to mark complete/incomplete
  - 44px touch target for mobile devices
  - Bounces on completion for visual feedback
- **Task Content** (center):
  - Title (bold, larger font)
  - Description (smaller, gray)
  - Tags (colored pills)
  - Due date (with clock icon)
  - Recurrence pattern (if recurring)
- **Action Buttons** (right):
  - Edit button (pencil icon)
  - Delete button (trash icon)
  - Visible on hover (desktop) or always visible (mobile)
- **Priority Indicator** (top-right corner):
  - Small colored dot (red/orange/blue)
  - Subtle background circle

**Task Card Colors:**
- Each task gets a unique color from a palette of 8 colors
- Colors are assigned based on task ID (consistent across sessions)
- Includes pink, purple, green, blue, orange, and rose variations

### Editing Tasks

1. **Click the pencil icon** on any task card
2. **Or use keyboard**: Tab to the task, Tab to edit button, press Enter
3. Modify any fields
4. Click "Update Task" or press Enter to save
5. Changes are saved immediately to the database
6. Toast notification confirms the update

### Deleting Tasks

1. **Click the trash icon** on any task card
2. **Confirmation required**: A dialog will ask you to confirm
3. Click "Delete" to permanently remove the task
4. **Undo feature** (future enhancement)

### Marking Tasks Complete

**Method 1: Click checkbox**
- Click the checkbox on the left side of the task card
- Task opacity reduces to 60% when completed
- Title gets strikethrough styling
- Checkmark icon bounces for visual feedback

**Method 2: Keyboard**
- Tab to the checkbox
- Press Space to toggle

**Completion Effects:**
- Visual animation (bounce)
- Screen reader announcement: "Task marked as complete"
- Task moves according to current sort/filter settings

---

## Search and Filtering

### Search Functionality

**Search Bar:**
- Located at the top of the page (command bar)
- Placeholder: "Search tasks... (Press / to focus)"
- **Debounced search**: 300ms delay to reduce API calls while typing
  - Type normally - the search will trigger after you stop typing
  - Immediate visual feedback (value updates instantly)
  - Optimized for performance

**What You Can Search:**
- Task titles
- Task descriptions
- Tags (full or partial match)

**Keyboard Shortcut:**
- Press `/` anywhere to focus the search input
- Start typing immediately
- Press `Esc` to clear focus

**Search Tips:**
- Use keywords from title, description, or tags
- Search is case-insensitive
- Partial matches are supported
- Results update automatically as you type (after 300ms)

### Filtering Tasks

**Opening Filters:**
- Click the "Filter" button in the command bar
- Or press `F` (keyboard shortcut)
- Filter panel slides down below the command bar

**Filter Options:**

**1. Priority Filter (Multi-Select)**
- Check any combination of:
  - ☐ High
  - ☐ Medium
  - ☐ Low
- Tasks matching ANY selected priority will be shown
- Uncheck all to show all priorities

**2. Status Filter (Single-Select)**
- Radio buttons for:
  - ⦿ All (default)
  - ○ Pending (incomplete tasks)
  - ○ Completed (completed tasks)
- Only one can be selected at a time

**Reset Filters:**
- Click "Reset Filters" at the bottom of the filter panel
- Clears all filters and search
- Returns to default view (all tasks)

### Sorting Tasks

**Opening Sort Panel:**
- Click the "Sort" button in the command bar
- Sort panel slides down below the command bar

**Sort By Options:**
- ○ Date Created (default)
- ○ Due Date
- ○ Priority
- ○ Last Updated

**Sort Order:**
- ○ Ascending (A→Z, Old→New)
- ○ Descending (Z→A, New→Old)

**How It Works:**
- Select a sort field and order
- Tasks are immediately re-ordered
- Sorting persists during your session
- Default: Created date, descending (newest first)

**Sort Behavior:**
- **Priority sorting**: High → Medium → Low (or reverse)
- **Date sorting**: Chronological or reverse chronological
- **Tasks without due dates**: Appear at the end when sorting by due date

---

## Keyboard Navigation

See [KEYBOARD_SHORTCUTS.md](./KEYBOARD_SHORTCUTS.md) for complete documentation.

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `N` | Create new task |
| `/` | Focus search |
| `F` | Toggle filters |
| `Esc` | Close modals |
| `Tab` | Navigate forward |
| `Shift+Tab` | Navigate backward |
| `Enter` | Submit / Confirm |
| `Space` | Toggle checkbox |

### Navigation Best Practices

1. **Learn the shortcuts**: Memorize `N`, `/`, `F`, and `Esc`
2. **Use Tab**: Navigate through all interactive elements
3. **Visual feedback**: Look for focus indicators (borders, shadows)
4. **Keyboard-only workflow**: Possible to use the entire app without a mouse

---

## Settings and Profile

### Accessing Settings

1. **Click the gear icon** in the sidebar (bottom-left)
2. Or navigate to `/dashboard/settings`
3. Settings page has three tabs:
   - Profile
   - Notifications
   - Keyboard Shortcuts

### Profile Settings

**Update Name:**
1. Go to Settings → Profile
2. Edit the "Name" field
3. Click "Save Changes"
4. Toast notification confirms the update
5. Name updates in navigation bar immediately

**Change Password:**
1. Go to Settings → Profile
2. Scroll to "Change Password" section
3. Enter current password
4. Enter new password (minimum 8 characters)
5. Confirm new password
6. Click "Change Password"
7. Toast notification confirms success

**Email:**
- Email is displayed but cannot be changed
- This is for security reasons
- Contact support if you need to change your email

### Notifications Settings

**Email Notifications:**
- ☐ Task reminders (future feature)
- ☐ Daily summary (future feature)
- ☐ Weekly summary (future feature)

**Push Notifications:**
- ☐ Browser notifications (future feature)
- ☐ Task due soon alerts (future feature)

**Note**: Notification features are planned for future releases.

### Keyboard Shortcuts Reference

The Settings → Keyboard Shortcuts tab provides a visual reference:
- Grouped by category (Navigation, Task Actions, etc.)
- Visual keyboard keys showing which keys to press
- Descriptions of what each shortcut does
- Always accessible for quick lookup

---

## Animations and Visual Feedback

### Task List Animations

**Initial Load:**
- Tasks fade in smoothly (`animate-fade-in`)
- Tasks slide up one by one with staggered delays
- Each task delays by 50ms after the previous one
- Creates a pleasant cascading effect

**Task Completion:**
- Checkbox shows a bouncing checkmark (`animate-bounce-subtle`)
- Task opacity reduces to 60%
- Title gets strikethrough styling
- Smooth transitions (200ms)

**Task Card Hover (Desktop):**
- Card scales up slightly (1.02x)
- Shadow becomes more prominent
- Edit/delete buttons fade in
- Smooth transitions for all effects

### Loading States

**Skeleton Loaders:**
- Instead of spinners, see placeholder cards
- Shows expected layout structure
- Pulse animation on placeholder elements
- Gives visual feedback about what's loading
- Improves perceived performance

**Where Skeleton Loaders Appear:**
- Initial task list load
- After filtering/sorting (if query is slow)
- Settings page tab switches (lazy-loaded components)

### Settings Page Animations

**Code Splitting with Lazy Loading:**
- Each settings tab loads only when activated
- Shows `SettingsLoader` (pulsing placeholders) while loading
- Components load quickly (typically < 100ms)
- Reduces initial bundle size

**Tab Switching:**
- Smooth fade-in when switching tabs
- Staggered animation delays (100ms, 200ms)
- Content appears gracefully

---

## Accessibility Features

This application is built with accessibility as a core principle, meeting **WCAG 2.1 Level AAA** standards.

### Screen Reader Support

**ARIA Live Announcements:**
- Task created: "Task created successfully"
- Task updated: "Task updated successfully"
- Task deleted: "Task deleted"
- Task restored: "Task restored"
- Task toggled: "Task marked as complete/incomplete"

**ARIA Labels:**
- All buttons have descriptive labels
- Example: "Edit task: Buy groceries" (includes task name)
- Icons marked `aria-hidden="true"` to prevent duplicate announcements
- Form inputs have associated labels

**Landmarks:**
- `<nav>` for navigation areas
- `<main>` for main content
- `<aside>` for sidebar
- Proper heading hierarchy (h1 → h2 → h3)

### Keyboard Accessibility

**Full Keyboard Navigation:**
- Every feature accessible without a mouse
- Tab order is logical and sequential
- Focus indicators on all interactive elements
- Skip links for quick navigation (future enhancement)

**Touch Targets:**
- **Minimum size**: 44px × 44px
- Meets WCAG Level AAA requirements
- Applies to: buttons, checkboxes, links, form inputs
- Easier to tap on mobile devices
- Reduces errors for users with motor impairments

### Visual Accessibility

**High Contrast:**
- Clear text colors on backgrounds
- Focus indicators with sufficient contrast
- Border and shadow for visual separation
- Color is not the only indicator (icons + text)

**Focus Indicators:**
- Visible focus rings on all interactive elements
- Consistent styling across the app
- Ring color: seal-brown with 30% opacity
- 2px ring thickness

**Font and Sizing:**
- Base font size: 16px (browser default)
- Relative sizing (rem units)
- Scales with browser zoom
- Clear font weights (normal, medium, semibold, bold)

---

## Performance Optimizations

### Debounced Search

**How It Works:**
- You type in the search box
- Value updates immediately (local state)
- After 300ms of no typing, search is sent to server
- Reduces API calls from hundreds to just a few

**Benefits:**
- Faster perceived performance
- Reduced server load
- Lower bandwidth usage
- Better battery life on mobile devices

**Example:**
```
Type: "b" → wait → "bu" → wait → "buy" → wait → "buy g" → wait...
API calls: 0... 0... 0... 0... 1 (after 300ms of no typing)
```

### React.memo Optimization

**ColorfulTaskCard Component:**
- Wrapped with `React.memo`
- Prevents re-renders when props haven't changed
- Important for long task lists (50+ tasks)
- Reduces CPU usage and improves frame rate

**When It Helps:**
- Scrolling through task list (smoother)
- Toggling one task (others don't re-render)
- Updating filters (only affected tasks re-render)

### Code Splitting

**Settings Page:**
- Profile, Notifications, and Keyboard Shortcuts tabs load on-demand
- Each component is in a separate JavaScript chunk
- Reduces initial bundle size by ~30KB
- Faster initial page load

**How It Works:**
```javascript
// Lazy loading
const ProfileSettings = lazy(() => import("@/components/settings/ProfileSettings"));

// Suspense for loading state
<Suspense fallback={<SettingsLoader />}>
  {activeTab === "profile" && <ProfileSettings />}
</Suspense>
```

**Benefits:**
- Faster initial load
- Pay-for-what-you-use model
- Better Core Web Vitals scores
- Improved SEO (if applicable)

---

## Tips and Tricks

### Power User Workflow

**Quick Task Creation:**
1. Press `N` (opens task form)
2. Type title
3. Press `Tab`, type description
4. Press `Enter` to save

**Efficient Searching:**
1. Press `/` (focuses search)
2. Type query
3. Use arrow keys to navigate results (future enhancement)
4. Press `Esc` to clear search

**Fast Filtering:**
1. Press `F` (opens filters)
2. Use `Tab` + `Space` to select priorities
3. Press `Esc` to apply filters

### Mobile Tips

**Touch Gestures:**
- Tap checkbox to toggle completion
- Tap edit/delete buttons (always visible on mobile)
- Swipe gestures (future enhancement)

**Responsive Layout:**
- Sidebar collapses on mobile
- Navigation moves to bottom (future enhancement)
- Task cards stack vertically
- All buttons meet 44px minimum size

### Task Organization

**Use Tags Effectively:**
- Create tags for projects: `@work`, `@personal`, `@urgent`
- Use tags for contexts: `@home`, `@office`, `@computer`, `@phone`
- Use tags for energy levels: `@quick`, `@focus`, `@creative`

**Priority System:**
- High: Must do today / urgent
- Medium: Should do this week
- Low: Nice to have / someday

**Due Dates:**
- Set realistic deadlines
- Use relative dates (today, tomorrow, next week)
- Filter by due date to see what's urgent

---

## Troubleshooting

### Common Issues

**Issue: Search not working**
- **Solution**: Wait 300ms after typing (debounced)
- **Check**: Network tab in dev tools for API calls

**Issue: Keyboard shortcuts not working**
- **Solution**: Click outside input fields, then try again
- **Exception**: `/` and `Esc` work everywhere

**Issue: Tasks not updating**
- **Solution**: Check internet connection
- **Check**: Browser console for errors
- **Try**: Refresh the page

**Issue: Slow performance**
- **Solution**: Clear browser cache
- **Check**: Disable browser extensions
- **Try**: Use a modern browser (Chrome, Firefox, Edge)

### CORS Errors

**Symptom**: "Unable to connect to server" error
- **Cause**: Backend CORS configuration doesn't include frontend port
- **Solution**: Add frontend port to `backend/.env` CORS_ORIGINS
- **Example**: `CORS_ORIGINS=...,http://localhost:3003`

### Authentication Issues

**Symptom**: Logged out unexpectedly
- **Cause**: Refresh token expired (7 days)
- **Solution**: Log in again
- **Prevention**: Use "Remember me" (future feature)

**Symptom**: "Invalid token" error
- **Cause**: Access token expired and refresh failed
- **Solution**: Log out and log in again
- **Check**: Backend server is running

---

## Advanced Features

### Recurring Tasks (Future Enhancement)

- Set tasks to repeat daily, weekly, monthly
- Automatic creation of next instance when completed
- Recurrence patterns displayed on task cards

### Collaboration (Future Enhancement)

- Share tasks with other users
- Assign tasks to team members
- Comment threads on tasks
- Activity feed for shared tasks

### Integrations (Future Enhancement)

- Google Calendar sync
- Email notifications
- Mobile app with push notifications
- API for third-party integrations

---

## Keyboard Shortcuts Quick Reference

For complete documentation, see [KEYBOARD_SHORTCUTS.md](./KEYBOARD_SHORTCUTS.md).

**Navigation:**
- `N` - New task
- `/` - Focus search
- `F` - Toggle filters
- `Esc` - Close overlays
- `Tab` - Next element
- `Shift+Tab` - Previous element

**Actions:**
- `Enter` - Submit / Confirm
- `Space` - Toggle checkbox

**In-App Reference:**
- Settings → Keyboard Shortcuts tab

---

## Getting Help

### Documentation

- [README.md](./README.md) - Project overview and setup
- [KEYBOARD_SHORTCUTS.md](./KEYBOARD_SHORTCUTS.md) - Complete keyboard reference
- [MANUAL_TESTING.md](./MANUAL_TESTING.md) - Testing guide (for developers)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide (for developers)

### Support

- **Issues**: Report bugs on GitHub Issues
- **Feature Requests**: Submit via GitHub Discussions
- **Email**: [Add support email here]

---

**Last Updated**: 2026-01-05
**Version**: Phase II UI Enhancements Complete
**Application Version**: 2.0.0
