# Phase III Frontend Implementation Plan

**Feature:** AI Chatbot Interface for Natural Language Task Management
**Status:** Planning
**Backend:** ✅ Complete and tested (22/22 tests passing)
**OpenAI API:** ✅ Working with sufficient credits

---

## 🎯 Objective

Build a chat interface where users can manage their todos using natural language:
- "Remind me to call mom tomorrow" → Creates task
- "Show my tasks" → Lists tasks
- "Mark task 5 as done" → Completes task
- "Delete the grocery task" → Deletes task

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /chat - Chat Interface Page                         │  │
│  │  ├─ ChatInterface Component (main container)         │  │
│  │  ├─ MessageList Component (displays history)         │  │
│  │  ├─ ChatInput Component (user input field)           │  │
│  │  └─ TaskActionCard Component (show task operations)  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Client (fetch to backend)                       │  │
│  │  └─ POST /api/chat with JWT token                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│  POST /api/chat                                              │
│  ├─ Authentication (JWT)                                     │
│  ├─ Rate Limiting (100/hour)                                 │
│  ├─ ChatbotService                                           │
│  │  ├─ IntentClassifier (OpenAI)                             │
│  │  ├─ TaskResolution                                        │
│  │  ├─ ActionExecutor (MCP Tools)                            │
│  │  └─ ResponseFormatter                                     │
│  └─ Save to Database (conversations, messages)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
frontend/src/
├── app/
│   └── chat/
│       └── page.tsx                    [NEW] Main chat page route
│
├── components/
│   └── chat/
│       ├── ChatInterface.tsx           [NEW] Main chat container
│       ├── MessageList.tsx             [NEW] Display messages
│       ├── ChatInput.tsx               [NEW] User input field
│       ├── TaskActionCard.tsx          [NEW] Show task operations
│       └── WelcomeScreen.tsx           [NEW] Empty state UI
│
├── lib/
│   └── api/
│       └── chat.ts                     [NEW] API client functions
│
└── types/
    └── chat.ts                         [NEW] TypeScript interfaces
```

**Total New Files:** 8
**Modified Files:** 1 (add navigation link)

---

## 🎨 Component Breakdown

### 1. `/chat` Page (`frontend/src/app/chat/page.tsx`)

**Purpose:** Main route for chat interface
**Protection:** Requires authentication (redirect to /login if not authenticated)

```typescript
// Key features:
- Server-side auth check
- Layout with header/sidebar
- Renders ChatInterface component
- SEO metadata (title, description)
```

**Estimated LOC:** ~80 lines

---

### 2. ChatInterface Component (`components/chat/ChatInterface.tsx`)

**Purpose:** Main container managing chat state and logic

**State Management:**
```typescript
const [messages, setMessages] = useState<Message[]>([])
const [input, setInput] = useState('')
const [isLoading, setIsLoading] = useState(false)
const [conversationId, setConversationId] = useState<string | null>(null)
```

**Key Functions:**
- `handleSendMessage()` - Send user message to backend
- `loadConversationHistory()` - Fetch previous messages
- `handleTaskAction()` - Process task operation results

**Features:**
- Auto-scroll to bottom on new message
- Loading states (typing indicator)
- Error handling with toast notifications
- Conversation persistence

**Estimated LOC:** ~200 lines

---

### 3. MessageList Component (`components/chat/MessageList.tsx`)

**Purpose:** Display conversation history

**Message Types:**
1. **User messages** - Right-aligned, blue background
2. **AI messages** - Left-aligned, gray background
3. **System messages** - Centered, muted (e.g., "Task created")

**Features:**
- Markdown rendering for AI responses
- Timestamp display (relative: "2 minutes ago")
- User/AI avatar icons
- Task action cards embedded in messages

**Example:**
```
┌─────────────────────────────────────────┐
│ 👤 You (2:45 PM)                        │
│ Remind me to buy groceries tomorrow     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🤖 AI Assistant (2:45 PM)               │
│ ✓ Created task: 'buy groceries'        │
│ ID: 42 | Due: Jan 16, 2026              │
│                                          │
│ ┌───────────────────────────────────┐  │
│ │ 📋 Task Created                    │  │
│ │ • Title: buy groceries             │  │
│ │ • Due: Tomorrow (Jan 16)           │  │
│ │ • Priority: medium                 │  │
│ └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Estimated LOC:** ~150 lines

---

### 4. ChatInput Component (`components/chat/ChatInput.tsx`)

**Purpose:** User input field with send button

**Features:**
- Textarea with auto-resize (max 5 lines)
- Send on Enter (Shift+Enter for new line)
- Disabled during loading
- Character counter (optional)
- Placeholder: "Type your message... (e.g., 'show my tasks')"

**UI:**
```
┌────────────────────────────────────────────────┐
│ Type your message...                      [📤] │
└────────────────────────────────────────────────┘
```

**Estimated LOC:** ~100 lines

---

### 5. TaskActionCard Component (`components/chat/TaskActionCard.tsx`)

**Purpose:** Visual card showing task operations

**Props:**
```typescript
interface TaskActionCardProps {
  action: 'create' | 'update' | 'delete' | 'complete' | 'list'
  task?: Task
  tasks?: Task[]
}
```

**Variants:**

**Create/Update:**
```
┌───────────────────────────────┐
│ ✅ Task Created                │
│ • Buy groceries               │
│ • Due: Tomorrow               │
│ • Priority: High              │
└───────────────────────────────┘
```

**List:**
```
┌───────────────────────────────┐
│ 📋 Your Tasks (3)              │
│ 1. ☐ Buy groceries (High)     │
│ 2. ☑ Call mom                 │
│ 3. ☐ Finish project report    │
└───────────────────────────────┘
```

**Estimated LOC:** ~120 lines

---

### 6. WelcomeScreen Component (`components/chat/WelcomeScreen.tsx`)

**Purpose:** Empty state when no messages

**Content:**
```
┌──────────────────────────────────────────┐
│            🤖                            │
│     AI Todo Assistant                    │
│                                          │
│  Try asking:                             │
│  • "Show my tasks"                       │
│  • "Remind me to call mom tomorrow"      │
│  • "Mark task 5 as done"                 │
│  • "Delete the grocery task"             │
└──────────────────────────────────────────┘
```

**Estimated LOC:** ~60 lines

---

### 7. API Client (`lib/api/chat.ts`)

**Purpose:** HTTP client for chat endpoint

**Functions:**
```typescript
export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  // POST /api/chat with JWT token
  // Returns: { response, conversation_id, intent, success }
}

export async function getConversationHistory(
  conversationId: string
): Promise<Message[]> {
  // GET /api/conversations/{id}/messages
  // Returns array of messages
}
```

**Error Handling:**
- 401: Redirect to login
- 429: Rate limit error with countdown
- 500: Generic error toast

**Estimated LOC:** ~80 lines

---

### 8. TypeScript Types (`types/chat.ts`)

**Purpose:** Type definitions

```typescript
export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  intent?: string
  taskAction?: TaskAction
}

export interface ChatResponse {
  response: string
  conversation_id: string
  intent: string
  success: boolean
  correlation_id: string
}

export interface TaskAction {
  type: 'create' | 'update' | 'delete' | 'complete' | 'list'
  task?: Task
  tasks?: Task[]
}
```

**Estimated LOC:** ~50 lines

---

## 🎭 User Flows

### Flow 1: First Time User
```
1. User navigates to /chat
2. Sees WelcomeScreen with suggestions
3. Types "show my tasks"
4. Presses Enter
5. Message appears in chat (right side)
6. Loading indicator shows (3 dots)
7. AI response appears (left side)
8. TaskActionCard shows list of tasks
9. Conversation saved with new conversation_id
```

### Flow 2: Create Task
```
1. User: "remind me to buy groceries tomorrow"
2. AI: "✓ Created task: 'buy groceries' (ID: 42)"
3. TaskActionCard shows:
   - Title: buy groceries
   - Due: Jan 16, 2026
   - Priority: medium
4. User can click "View All Tasks" → Navigate to /dashboard
```

### Flow 3: Error Handling
```
1. User sends message
2. Rate limit exceeded (429 error)
3. Toast notification: "Rate limit exceeded. Try again in 5 minutes."
4. Input field disabled with countdown timer
5. After cooldown, input re-enabled
```

### Flow 4: Continuing Conversation
```
1. User returns to /chat
2. Load last conversation from localStorage
3. Fetch message history from backend
4. Display full conversation
5. User continues chatting in same context
```

---

## 🎨 Design System (Using Existing shadcn/ui)

**Components Used:**
- `Button` - Send button
- `Card` - TaskActionCard, WelcomeScreen
- `Input` / `Textarea` - ChatInput
- `ScrollArea` - MessageList container
- `Toast` - Error notifications
- `Skeleton` - Loading states
- `Avatar` - User/AI icons

**Color Scheme:**
- User messages: `bg-blue-500 text-white`
- AI messages: `bg-gray-100 text-gray-900`
- System messages: `bg-yellow-50 text-yellow-800`
- Task cards: `bg-white border border-gray-200`

**Typography:**
- Messages: `text-sm`
- Timestamps: `text-xs text-gray-500`
- Task titles: `font-medium`

---

## 🔌 Backend Integration

### API Endpoint: `POST /api/chat`

**Request:**
```json
{
  "message": "remind me to buy groceries tomorrow",
  "conversation_id": "uuid-or-null"
}
```

**Response:**
```json
{
  "response": "✓ Created task: 'buy groceries' (ID: 42). Due: 2026-01-16.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "create_task",
  "success": true,
  "correlation_id": "abc123-def456"
}
```

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Rate Limiting:**
- 100 requests per hour per user
- Returns 429 with error detail when exceeded

---

## 🧪 Testing Strategy

### Manual Testing Checklist

**Authentication:**
- [ ] Redirect to /login when not authenticated
- [ ] Chat works when authenticated
- [ ] Token refresh handled correctly

**Chat Functionality:**
- [ ] Send message appears immediately
- [ ] AI response appears after API call
- [ ] Loading indicator shows during request
- [ ] Conversation persists across page refresh

**Task Operations:**
- [ ] Create task: "remind me to X"
- [ ] List tasks: "show my tasks"
- [ ] Complete task: "mark task 5 as done"
- [ ] Delete task: "delete task 3"
- [ ] Update task: "change task 2 to high priority"

**Error Handling:**
- [ ] Rate limit error shows countdown
- [ ] Network error shows toast
- [ ] Invalid token redirects to login
- [ ] Empty message doesn't send

**UI/UX:**
- [ ] Auto-scroll to bottom on new message
- [ ] Timestamps display correctly
- [ ] Mobile responsive
- [ ] Keyboard shortcuts work (Enter to send)

### Automated Tests (Future)

```typescript
// frontend/tests/chat.test.tsx
describe('ChatInterface', () => {
  it('sends message when user presses Enter')
  it('displays AI response after API call')
  it('shows loading state during request')
  it('handles rate limit errors gracefully')
})
```

---

## 📊 Implementation Timeline

### Phase 1: Core Structure (30 min)
- [ ] Create file structure
- [ ] Set up types and interfaces
- [ ] Build API client

### Phase 2: Components (90 min)
- [ ] ChatInput component
- [ ] MessageList component
- [ ] TaskActionCard component
- [ ] WelcomeScreen component
- [ ] ChatInterface container

### Phase 3: Integration (45 min)
- [ ] Connect to backend API
- [ ] Add authentication flow
- [ ] Implement error handling
- [ ] Add loading states

### Phase 4: Polish (30 min)
- [ ] Styling and responsiveness
- [ ] Animations (fade in, slide up)
- [ ] Accessibility (ARIA labels, keyboard nav)
- [ ] Toast notifications

### Phase 5: Testing (45 min)
- [ ] Manual testing all user flows
- [ ] Test error scenarios
- [ ] Mobile testing
- [ ] Cross-browser check

**Total Estimated Time:** 3-4 hours

---

## 🚀 Deployment Considerations

**Environment Variables:**
- `NEXT_PUBLIC_API_URL` - Backend URL (already set)

**Build Process:**
```bash
cd frontend
npm run build
npm run start
```

**Performance:**
- Lazy load chat page (only loads when accessed)
- Debounce typing indicator
- Pagination for long conversations (future)

**Security:**
- All API calls use JWT authentication
- No sensitive data in localStorage (only conversation_id)
- CORS configured correctly

---

## 📈 Success Metrics

**What Success Looks Like:**
1. ✅ User can create tasks via natural language
2. ✅ AI correctly classifies intent (>90% accuracy)
3. ✅ Conversation history persists
4. ✅ Error handling is graceful
5. ✅ Mobile responsive
6. ✅ No Phase II regressions

**Acceptance Criteria:**
- [ ] All 5 intents work (create, list, update, delete, complete)
- [ ] Rate limiting doesn't break UX
- [ ] Chat UI matches design system
- [ ] Loading states are clear
- [ ] Errors show helpful messages

---

## 🔄 Future Enhancements (Not in This Phase)

- Voice input (speech-to-text)
- Markdown formatting in messages
- Message reactions (👍 👎)
- Export conversation to PDF
- Multi-language support
- Streaming responses (OpenAI streaming API)
- Task suggestions based on history
- Smart scheduling ("tomorrow 2pm")

---

## 📋 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OpenAI quota exceeded | Low | High | Graceful fallback message, retry logic |
| Rate limiting affects UX | Medium | Medium | Clear countdown, queue messages |
| Intent classification inaccurate | Low | Medium | Confidence threshold (0.7), ask for clarification |
| Mobile keyboard issues | Low | Low | Test on real devices |
| Conversation history large | Low | Medium | Pagination (future), limit to 100 messages |

---

## 🎯 Decision Points

**Before I proceed, please confirm:**

1. **Design Approach:** Simple, clean chat UI (like WhatsApp/ChatGPT)?
2. **Conversation Persistence:** Save full history in DB? ✅ Yes (spec requirement)
3. **Navigation:** Add "Chat" link to header? ✅ Yes
4. **Welcome Screen:** Show example prompts? ✅ Yes
5. **Task Actions:** Show visual cards for task operations? ✅ Yes

---

## ✅ Ready to Implement

**This plan delivers:**
- 8 new files (~840 lines of code)
- Clean, maintainable architecture
- Full integration with tested backend
- Professional UI/UX
- Comprehensive error handling

**Estimated delivery:** 3-4 hours of focused work

**Total Phase III LOC (Backend + Frontend):**
- Backend: ~656 lines (NFR + tests)
- Frontend: ~840 lines (UI components)
- **Grand Total: ~1,500 lines** for complete AI chatbot feature

---

## 🚦 Next Steps

**If you approve this plan, I'll proceed in this order:**

1. Create file structure and types
2. Build API client
3. Build components (bottom-up: Input → Message → List → Interface)
4. Integrate with backend
5. Add error handling and polish
6. Manual testing
7. Deploy and demo

**Reply "approved" to start implementation** or ask questions about any section.
