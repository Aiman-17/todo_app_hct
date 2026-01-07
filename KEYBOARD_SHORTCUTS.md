# Keyboard Shortcuts Guide

This document provides a comprehensive reference for all keyboard shortcuts available in the Todo Application.

## Quick Reference

| Shortcut | Action | Context |
|----------|--------|---------|
| `N` | Create new task | Anywhere (except input fields) |
| `/` | Focus search input | Anywhere |
| `F` | Toggle filters panel | Anywhere (except input fields) |
| `Esc` | Close modals/dropdowns | Anywhere |
| `Tab` | Navigate between elements | Anywhere |
| `Shift + Tab` | Navigate backwards | Anywhere |
| `Enter` | Submit forms / Confirm actions | Forms and buttons |
| `Space` | Toggle checkboxes | Focused checkbox |

## Navigation Shortcuts

### Global Navigation

**N - New Task**
- **When**: Press `N` anywhere in the application (except when typing in input fields)
- **Action**: Opens the "Create New Task" dialog
- **Example**: While viewing your task list, press `N` to quickly add a new task

**/ - Focus Search**
- **When**: Press `/` anywhere in the application
- **Action**: Focuses the search input field in the command bar
- **Example**: Press `/` to quickly start searching without clicking the search box
- **Note**: Works even when typing in other fields for quick context switching

**F - Toggle Filters**
- **When**: Press `F` anywhere in the application (except when typing in input fields)
- **Action**: Opens or closes the filters panel
- **Example**: Press `F` to quickly filter tasks by priority and status

**Esc - Close Overlays**
- **When**: Press `Esc` anywhere in the application
- **Action**: Closes the currently open modal, dialog, or dropdown
- **Example**: Press `Esc` to close the task creation dialog without saving

### Tab Navigation

**Tab - Move Forward**
- **When**: Press `Tab` anywhere in the application
- **Action**: Moves keyboard focus to the next interactive element
- **Example**: Navigate through form fields, buttons, and links sequentially
- **Accessibility**: All interactive elements have visible focus indicators

**Shift + Tab - Move Backward**
- **When**: Press `Shift + Tab` anywhere in the application
- **Action**: Moves keyboard focus to the previous interactive element
- **Example**: Navigate backwards through the interface

## Task Actions

### Task Interaction

**Enter - Submit / Confirm**
- **When**: Press `Enter` when a button or form is focused
- **Action**: Submits the form or activates the focused button
- **Examples**:
  - In task form: Saves the task
  - On delete button: Confirms deletion
  - On save button: Saves changes

**Space - Toggle Checkbox**
- **When**: Press `Space` when a checkbox is focused
- **Action**: Toggles the checkbox state (checked ↔ unchecked)
- **Examples**:
  - Task completion checkbox: Marks task as complete/incomplete
  - Filter checkboxes: Selects/deselects filter options

## Screen Reader Support

The application fully supports keyboard-only navigation and screen readers. Key features:

### ARIA Live Announcements

The application announces important actions to screen readers:
- **Task Created**: "Task created successfully"
- **Task Updated**: "Task updated successfully"
- **Task Deleted**: "Task deleted"
- **Task Restored**: "Task restored" (after undo)
- **Task Toggled**: "Task marked as complete" / "Task marked as incomplete"

### ARIA Labels

All interactive elements have descriptive ARIA labels:
- Buttons include action context (e.g., "Edit task: Buy groceries")
- Icons are marked with `aria-hidden="true"` to prevent redundant announcements
- Regions are properly labeled (navigation, main content, complementary)

### Semantic HTML

- Proper heading hierarchy (h1 → h2 → h3)
- Navigation landmarks with `<nav role="navigation">`
- Form labels associated with inputs
- Tab panels with proper `role="tabpanel"` and `aria-labelledby`

## Accessibility Standards

This application meets **WCAG 2.1 Level AAA** guidelines:

### Touch Targets
- **Minimum size**: 44px × 44px for all interactive elements
- **Application**: Buttons, checkboxes, form inputs, and links

### Focus Indicators
- **Visible focus rings** on all interactive elements
- **High contrast** borders and outlines
- **Consistent styling** across the application

### Keyboard-Only Navigation
- **No mouse required**: All functionality accessible via keyboard
- **Logical tab order**: Elements focused in a meaningful sequence
- **Skip links**: (Future enhancement for quick navigation)

## Best Practices

### For Keyboard Users

1. **Learn the shortcuts**: Memorize `N`, `/`, `F`, and `Esc` for efficient navigation
2. **Use Tab liberally**: Tab navigation is your friend for discovering interface elements
3. **Visual feedback**: Watch for focus indicators to know where you are
4. **Form navigation**: Use `Tab` to move between fields, `Enter` to submit

### For Screen Reader Users

1. **Navigation landmarks**: Use landmarks (navigation, main, complementary) to jump between sections
2. **Headings**: Navigate by headings to quickly find content
3. **ARIA live regions**: Listen for announcements after actions
4. **Form labels**: All inputs have associated labels read by screen readers

## Tips and Tricks

### Power User Workflow

```
1. Press / to focus search
2. Type search query
3. Press Esc to close search
4. Press F to open filters
5. Select filters with Tab and Space
6. Press Esc to close filters
7. Press N to create new task
8. Fill form with Tab navigation
9. Press Enter to submit
```

### Quick Task Creation

```
1. Press N (anywhere)
2. Type task title
3. Press Tab to move to description
4. Type description (optional)
5. Press Tab to navigate to priority/due date (optional)
6. Press Enter to save
```

### Efficient Filtering

```
1. Press F to open filters
2. Use Tab to navigate to priority checkboxes
3. Press Space to select priorities
4. Tab to status radio buttons
5. Use arrow keys to select status
6. Press Esc to close filters
```

## Troubleshooting

### Shortcut Not Working?

**Problem**: Pressing `N` or `F` does nothing

**Cause**: You're currently focused on an input field (search, task form, etc.)

**Solution**: Press `Esc` to exit the input field, then try the shortcut again

**Exception**: The `/` (search) and `Esc` (close) shortcuts work everywhere

---

### Focus Lost?

**Problem**: Can't see where keyboard focus is

**Cause**: Focus indicator might be subtle on some elements

**Solution**:
- Press `Tab` multiple times to cycle through elements
- Look for subtle border or shadow changes
- Use browser dev tools to inspect `:focus` styles

---

### Screen Reader Not Announcing?

**Problem**: Actions aren't being announced

**Cause**: ARIA live region might not be properly initialized

**Solution**:
- Refresh the page
- Ensure screen reader is running before loading the app
- Check screen reader settings for "announcements" or "live regions"

## In-App Reference

For a visual reference of all keyboard shortcuts, visit:

**Settings → Keyboard Shortcuts**

1. Navigate to the settings page (click gear icon in sidebar)
2. Click the "Keyboard Shortcuts" tab
3. View grouped shortcuts with visual keyboard keys

## Future Enhancements

Planned keyboard shortcuts for future versions:

- `Ctrl/Cmd + K`: Command palette for quick actions
- `Ctrl/Cmd + /`: Toggle keyboard shortcuts help overlay
- `Ctrl/Cmd + F`: Advanced search with filters
- Arrow keys: Navigate through task list
- `Del`: Delete focused task (with confirmation)
- Custom shortcuts: User-defined keyboard shortcuts

---

**Last Updated**: 2026-01-05
**Version**: Phase II UI Enhancements Complete
**WCAG Compliance**: Level AAA
