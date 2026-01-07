# Tasks: Phase II UI Enhancements - Premium Minimalist Design

**Feature**: 002-fullstack-web-auth (UI Enhancement Phase)
**Input**: User requirements for professional, minimalist, premium UI with advanced task management features
**Prerequisites**: Phase II basic auth and CRUD complete (tasks.md)
**Branch**: `002-ui-enhancements` (branch from `002-fullstack-web-auth`)

## Overview

This tasks file extends Phase II with a complete UI/UX redesign featuring:
- **Design System**: Rose White (#FFF0EB) background, Seal Brown (#2D0B00) text, Inter typography
- **Icon-First Interactions**: All actions use icons (add/edit/delete/complete/undo)
- **Card-Based Layout**: Soft shadows, rounded corners, subtle animations
- **Advanced Features**: Priorities, tags, recurring tasks, due dates, notifications
- **Responsive Design**: Full mobile/tablet/desktop support
- **Accessibility**: Keyboard navigation, screen reader support, ARIA labels
- **Bonus Features**: Multi-language (including Urdu), voice commands

**Tests**: Tests are OPTIONAL for this UI enhancement phase. Focus on visual/interactive QA.

---

## Phase 1: Design Foundation & Theme Setup

**Purpose**: Establish design system, custom color palette, and Tailwind configuration

- [X] T001 Update Tailwind config with custom colors (#FFF0EB, #2D0B00) in frontend/tailwind.config.ts
- [X] T002 [P] Install and configure Inter font in frontend/src/app/layout.tsx
- [X] T003 [P] Install lucide-react icons package in frontend/package.json
- [X] T004 [P] Create design tokens file in frontend/src/lib/design-tokens.ts
- [X] T005 Create global CSS with custom shadows and animations in frontend/src/app/globals.css
- [X] T006 [P] Add priority color variants to Tailwind config (high: #9C1F1F, medium: #FFB8A6, low: #FFE5DB)

---

## Phase 2: Core Layout Components

**Purpose**: Build main layout structure with sidebar, top bar, and floating action button

- [X] T007 Create icon-only sidebar component in frontend/src/components/layout/Sidebar.tsx
- [X] T008 [P] Create top command bar with search/filter/sort in frontend/src/components/layout/CommandBar.tsx
- [X] T009 [P] Create floating add-task button component in frontend/src/components/layout/FloatingAddButton.tsx
- [X] T010 Update dashboard layout to use new layout components in frontend/src/app/dashboard/layout.tsx
- [X] T011 [P] Add hover states and transitions to sidebar icons
- [X] T012 [P] Implement pulse animation for floating action button

---

## Phase 2.5: Enhanced Task List & Analytics (NEW REQUIREMENTS) ✅

**Purpose**: Implement colorful task cards, Pomodoro timer, and completion analytics based on design inspiration

- [x] T013 Update background color from #FFF0EB to #F5EDE6 in frontend/tailwind.config.ts and globals.css
- [x] T014 [P] Create colorful task card component with dynamic colors (pink, purple, green, blue, orange) in frontend/src/components/tasks/ColorfulTaskCard.tsx
- [x] T015 [P] Add task category icons (inspired by Pomodoro app design) in frontend/src/components/tasks/TaskIcon.tsx
- [x] T016 [P] Replace edit/delete buttons with icon buttons (Pencil, Trash icons from lucide-react)
- [x] T017 Update checkbox styling with modern rounded design
- [x] T018 Create task completion analytics component (circular progress indicator) in frontend/src/components/analytics/CompletionCircle.tsx
- [x] T019 [P] Create Pomodoro timer component with circular countdown in frontend/src/components/timer/PomodoroTimer.tsx
- [x] T020 [P] Add timer duration presets (5, 10, 20, 25, 60, 120 minutes)
- [x] T021 Integrate timer with task focus functionality
- [x] T022 Update TaskList to use new ColorfulTaskCard component

---

## Phase 3: Enhanced Data Model (Backend) ✅

**Purpose**: Extend Task model with priorities, tags, due dates, and recurrence

- [x] T023 Add priority field to Task model (enum: high/medium/low) in backend/src/models/task.py
- [x] T024 [P] Add due_date field (nullable datetime) to Task model in backend/src/models/task.py
- [x] T025 [P] Add tags field (JSON array) to Task model in backend/src/models/task.py
- [x] T026 [P] Add recurrence_rule field (JSON object) to Task model in backend/src/models/task.py
- [x] T027 Create database migration for new Task fields using Alembic in backend/alembic/versions/
- [x] T028 Update TaskCreate schema with new fields in backend/src/schemas/task.py
- [x] T029 [P] Update TaskUpdate schema with new fields in backend/src/schemas/task.py
- [x] T030 [P] Update TaskResponse schema with new fields in backend/src/schemas/task.py

---

## Phase 4: Enhanced Task Service (Backend) ✅

**Purpose**: Update service layer to handle priorities, tags, due dates, and recurrence

- [x] T021 Update create_task to accept priority, tags, due_date, recurrence in backend/src/services/task_service.py
- [x] T022 [P] Update update_task to handle all new fields in backend/src/services/task_service.py
- [x] T023 [P] Add filter_by_priority function in backend/src/services/task_service.py
- [x] T024 [P] Add filter_by_tags function in backend/src/services/task_service.py
- [x] T025 [P] Add filter_by_due_date function in backend/src/services/task_service.py
- [x] T026 [P] Add sort_by_priority function in backend/src/services/task_service.py
- [x] T027 [P] Add sort_by_due_date function in backend/src/services/task_service.py
- [x] T028 Implement soft delete with undo capability in backend/src/services/task_service.py

---

## Phase 5: Enhanced API Endpoints (Backend) ✅

**Purpose**: Expose new filtering, sorting, and soft delete endpoints

- [x] T029 Add GET /api/tasks?priority=high endpoint in backend/src/api/tasks.py
- [x] T030 [P] Add GET /api/tasks?tags=work,urgent endpoint in backend/src/api/tasks.py
- [x] T031 [P] Add GET /api/tasks?due_date=today endpoint in backend/src/api/tasks.py
- [x] T032 [P] Add GET /api/tasks?sort=priority endpoint in backend/src/api/tasks.py
- [x] T033 [P] Add GET /api/tasks?sort=due_date endpoint in backend/src/api/tasks.py
- [x] T034 [P] Add POST /api/tasks/{id}/undo-delete endpoint in backend/src/api/tasks.py
- [x] T035 Update task deletion to use soft delete in backend/src/api/tasks.py

---

## Phase 6: Premium Task Card Component ✅

**Purpose**: Redesign task cards with new visual design and interactive elements

- [x] T036 Create new TaskCard component with rose/brown theme in frontend/src/components/tasks/ColorfulTaskCard.tsx
- [x] T037 [P] Add priority dot indicator to TaskCard (colored based on priority level)
- [x] T038 [P] Add tags pills display to TaskCard (pill-shaped, muted tones)
- [x] T039 [P] Add relative due date label (Today, Tomorrow, In X days) to TaskCard
- [x] T040 [P] Implement hover state revealing edit/delete/complete icons
- [x] T041 [P] Add smooth transitions for card interactions (duration-200, ease-in-out)
- [x] T042 Update TaskList to use new TaskCard component in frontend/src/components/tasks/TaskList.tsx

---

## Phase 7: Enhanced Task Form ✅

**Purpose**: Add priority, tags, due date, and recurrence inputs to task creation/editing

- [x] T043 Add priority selector dropdown to TaskForm in frontend/src/components/tasks/TaskForm.tsx
- [x] T044 [P] Add tags input with add/remove functionality in frontend/src/components/tasks/TaskForm.tsx
- [x] T045 [P] Add due date picker component in frontend/src/components/tasks/TaskForm.tsx
- [x] T046 [P] Add recurrence rule selector (daily/weekly/monthly) in frontend/src/components/tasks/TaskForm.tsx
- [x] T047 [P] Update form validation to include new fields
- [x] T048 Update task creation API call to include new fields in frontend/src/lib/api.ts

---

## Phase 8: Search, Filter, and Sort UI ✅

**Purpose**: Implement real-time search, multi-select filters, and sort controls

- [x] T049 Implement live search input in CommandBar in frontend/src/components/layout/CommandBar.tsx
- [x] T050 [P] Add priority filter dropdown (multi-select) in frontend/src/components/layout/CommandBar.tsx
- [x] T051 [P] Add status filter dropdown (all/pending/completed) in frontend/src/components/layout/CommandBar.tsx
- [x] T052 [P] Add due date filter dropdown (today/tomorrow/this week/overdue) in frontend/src/components/layout/CommandBar.tsx
- [x] T053 [P] Add sort selector (created_at/due_date/priority/updated_at, asc/desc) in frontend/src/components/layout/CommandBar.tsx
- [x] T054 Implement filter/sort state management with React context in frontend/src/contexts/FilterContext.tsx
- [x] T055 Connect CommandBar filters to TaskList component via FilterContext and backend API

---

## Phase 9: User Preferences & Persistence ✅

**Purpose**: Save user preferences for filters, sorting, and theme in localStorage

- [x] T056 Enhanced FilterContext with localStorage persistence in frontend/src/contexts/FilterContext.tsx
- [x] T057 [P] Implement localStorage persistence for filter preferences (priority, status)
- [x] T058 [P] Implement localStorage persistence for sort preferences (sortBy, order)
- [x] T059 [P] Implement localStorage persistence for view mode (grid/list)
- [x] T060 Load saved preferences on app startup with SSR safety
- [x] T061 [P] Reset preferences via resetFilters() function (clears localStorage)

---

## Phase 10: Recurring Tasks Logic ✅

**Purpose**: Implement recurring task rules and display in dashboard

- [x] T062 Create recurring task calculation utility in frontend/src/lib/recurrence.ts
- [x] T063 [P] Add recurrence badge to TaskCard (shows "Daily", "Weekly", "Monthly")
- [x] T064 [P] Implement next occurrence calculation for recurring tasks
- [x] T065 Update task completion to handle recurring tasks (create next occurrence) in backend/src/services/task_service.py
- [x] T066 Add GET /api/tasks/upcoming endpoint for recurring task preview in backend/src/api/tasks.py

---

## Phase 11: Due Date & Notifications ✅

**Purpose**: Implement relative due date labels and browser notifications

- [x] T067 Create due date formatter utility (Today, Tomorrow, In X days) in frontend/src/lib/date-utils.ts
- [x] T068 [P] Add overdue highlighting to TaskCard (subtle red accent for overdue tasks)
- [x] T069 [P] Request browser notification permission in settings
- [x] T070 [P] Implement notification scheduling for due tasks
- [x] T071 Create notifications settings UI in frontend/src/components/settings/NotificationsSettings.tsx
- [x] T072 [P] Add notification preferences to user preferences context

---

## Phase 12: Soft Delete & Undo ✅

**Purpose**: Implement soft delete with undo capability

- [x] T073 Update delete confirmation modal with undo toast in frontend/src/components/tasks/TaskList.tsx
- [x] T074 [P] Implement undo delete functionality with 5-second timeout
- [x] T075 [P] Add deleted_at field to Task model in backend/src/models/task.py
- [x] T076 [P] Update task queries to exclude soft-deleted tasks
- [x] T077 Create restore/undo endpoint POST /api/tasks/{task_id}/restore

---

## Phase 13: Responsive Design Refinements ✅

**Purpose**: Ensure perfect responsive behavior on all screen sizes

- [x] T078 Test and refine mobile layout (320px-767px) for all components
- [x] T079 [P] Test and refine tablet layout (768px-1023px) for all components
- [x] T080 [P] Test and refine desktop layout (1024px+) for all components
- [x] T081 [P] Ensure touch targets are min 44px×44px on mobile (checkbox: 44px, buttons: 44px)
- [ ] T082 [P] Add swipe gestures for mobile task actions (optional - not implemented)
- [x] T083 Verify sidebar collapses/expands appropriately on small screens

---

## Phase 14: Keyboard Navigation & Accessibility ✅

**Purpose**: Implement full keyboard navigation and screen reader support

- [x] T084 Add keyboard shortcuts (N: new task, /: search, F: filter, Escape) to CommandBar
- [x] T085 [P] Implement Tab navigation for all interactive elements
- [x] T086 [P] Add Escape key to close modals and dropdowns
- [x] T087 [P] Add Enter key to submit forms and confirm actions
- [x] T088 [P] Add ARIA labels to all icons and buttons
- [x] T089 [P] Add screen reader announcements for task operations (created, updated, deleted)
- [ ] T090 Test with keyboard-only navigation for all user flows
- [ ] T091 [P] Test with NVDA/JAWS screen reader

---

## Phase 15: Bonus - Multi-Language Support

**Purpose**: Add Urdu translation and multi-language support (OPTIONAL)

- [ ] T092 Install i18n library (next-intl or react-i18next) in frontend/package.json
- [ ] T093 [P] Create translation files (en.json, ur.json) in frontend/src/locales/
- [ ] T094 [P] Translate all UI text to Urdu (buttons, labels, placeholders)
- [ ] T095 [P] Add language switcher in settings
- [ ] T096 [P] Implement RTL layout support for Urdu
- [ ] T097 Test all features in Urdu language mode

---

## Phase 16: Bonus - Voice Commands

**Purpose**: Add voice input for task creation and management (OPTIONAL)

- [ ] T098 Integrate Web Speech API in frontend/src/lib/voice.ts
- [ ] T099 [P] Create floating microphone button component in frontend/src/components/voice/VoiceMicButton.tsx
- [ ] T100 [P] Implement speech-to-text for task title capture
- [ ] T101 [P] Add voice command parser (e.g., "create task buy groceries high priority")
- [ ] T102 [P] Add visual feedback for voice recording state
- [ ] T103 [P] Add voice command help modal with supported phrases
- [ ] T104 Test voice commands in quiet and noisy environments

---

## Phase 17: Animation & Motion Design ✅

**Purpose**: Add subtle animations and transitions for calm UX

- [x] T105 Add fade-in animation for task list loading in frontend/src/components/tasks/TaskList.tsx
- [x] T106 [P] Add slide-in animation for new tasks with staggered delays
- [x] T107 [P] Add scale animation for task completion (checkmark bounce)
- [x] T108 [P] Add fade-out animation for deleted tasks (supported via existing animations)
- [x] T109 [P] Implement skeleton loading states for async operations in frontend/src/components/shared/SkeletonTaskCard.tsx
- [x] T110 [P] Add smooth scroll behavior for long task lists (already in globals.css)
- [x] T111 Ensure all animations respect prefers-reduced-motion (already in globals.css)

---

## Phase 18: Settings & User Profile ✅

**Purpose**: Create settings page for user preferences and profile management

- [x] T112 Create settings page layout in frontend/src/app/dashboard/settings/page.tsx
- [x] T113 [P] Add profile section (name, email, password change) in frontend/src/components/settings/ProfileSettings.tsx
- [ ] T114 [P] Add appearance section (theme toggle if applicable) in frontend/src/components/settings/AppearanceSettings.tsx (skipped - no theme toggle needed)
- [x] T115 [P] Add notifications settings section (already created in Phase 11)
- [ ] T116 [P] Add language preferences section (if multi-language enabled) (skipped - Phase 15 optional)
- [x] T117 [P] Add keyboard shortcuts reference panel in frontend/src/components/settings/KeyboardShortcuts.tsx
- [ ] T118 Add profile update API endpoint in backend/src/api/auth.py (to be implemented when needed)

---

## Phase 19: Performance Optimization ✅

**Purpose**: Optimize frontend performance for large task lists

- [ ] T119 Implement virtual scrolling for large task lists (>100 tasks) in frontend/src/components/tasks/TaskList.tsx (skipped - not needed for current scale)
- [ ] T120 [P] Add pagination or infinite scroll for task loading (skipped - using client-side filtering)
- [x] T121 [P] Optimize re-renders with React.memo for ColorfulTaskCard component
- [x] T122 [P] Implement debouncing for search input (300ms delay in CommandBar with useDebounce hook)
- [x] T123 [P] Add loading skeletons instead of spinners (implemented SkeletonTaskCard in Phase 17)
- [x] T124 Optimize bundle size with code splitting and lazy loading for settings page components

---

## Phase 20: Testing & Quality Assurance

**Purpose**: Comprehensive testing across browsers and devices

- [ ] T125 Visual regression testing for all UI components
- [ ] T126 [P] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] T127 [P] Mobile device testing (iOS Safari, Android Chrome)
- [ ] T128 [P] Tablet device testing (iPad, Android tablets)
- [ ] T129 [P] Accessibility audit with Lighthouse
- [ ] T130 [P] Performance audit with Lighthouse
- [ ] T131 User acceptance testing with real users
- [ ] T132 [P] Fix any bugs or issues identified during testing

---

## Phase 21: Documentation & Polish

**Purpose**: Update documentation and final polish

- [ ] T133 Update README with new UI features and screenshots in README.md
- [ ] T134 [P] Create UI component style guide in docs/ui-style-guide.md
- [ ] T135 [P] Document keyboard shortcuts in docs/keyboard-shortcuts.md
- [ ] T136 [P] Update API documentation with new endpoints in backend/README.md
- [ ] T137 [P] Create user guide for advanced features in docs/user-guide.md
- [ ] T138 Add changelog entry for UI enhancements in CHANGELOG.md

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
Start with Phases 1-7 to get the core visual redesign and basic enhanced features:
- ✅ Design foundation (custom colors, Inter font)
- ✅ New layout (sidebar, command bar, floating button)
- ✅ Enhanced data model (priorities, tags, due dates)
- ✅ Premium task cards with new visual design

### Incremental Delivery
- **Week 1**: Phases 1-2 (Design foundation + layout)
- **Week 2**: Phases 3-5 (Backend enhancements)
- **Week 3**: Phases 6-7 (Premium task cards + enhanced form)
- **Week 4**: Phases 8-9 (Search/filter/sort + preferences)
- **Week 5**: Phases 10-12 (Recurring tasks + notifications + soft delete)
- **Week 6**: Phases 13-14 (Responsive design + accessibility)
- **Week 7+**: Bonus phases as time allows

### Parallel Opportunities
- Backend (Phases 3-5) and Frontend Design (Phases 1-2, 6-7) can run in parallel
- Most Phase 8-14 tasks marked [P] can run in parallel
- Testing (Phase 20) can start early with continuous integration

### Dependencies
- Phase 6-7 depend on Phase 3-5 (backend changes must be complete)
- Phase 8 depends on Phase 6 (need new TaskCard component)
- Phase 10-12 depend on Phase 3-5 (backend recurrence support)
- Phase 15-16 (bonus) are independent and can be added anytime

---

## Total Task Count: 138 tasks

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Layout)**: 6 tasks
- **Phase 3-5 (Backend)**: 23 tasks
- **Phase 6-7 (Task Card/Form)**: 13 tasks
- **Phase 8-9 (Search/Filter/Preferences)**: 13 tasks
- **Phase 10-12 (Recurring/Notifications/Undo)**: 16 tasks
- **Phase 13-14 (Responsive/A11y)**: 14 tasks
- **Phase 15-16 (Bonus Features)**: 13 tasks
- **Phase 17-21 (Polish/Testing/Docs)**: 34 tasks

**Parallelization**: ~60% of tasks marked [P] can run in parallel (83 tasks)

**Suggested MVP**: Phases 1-9 (68 tasks) delivers core visual redesign + enhanced task management
