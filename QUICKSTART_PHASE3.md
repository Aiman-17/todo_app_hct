# Quick Start: Phase III AI Chatbot

**⏱️ Setup Time**: 5 minutes

---

## 🚀 Step 1: Get Gemini API Key (1 min)

1. Visit: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

---

## 🔧 Step 2: Backend Setup (2 mins)

### Install Gemini SDK

```bash
cd backend
pip install google-generativeai>=0.3.0
```

### Configure API Key

Create or edit `backend/.env`:

```env
GEMINI_API_KEY=AIzaSy...your-key-here
DATABASE_URL=postgresql://...your-neon-db...
BETTER_AUTH_SECRET=your-32-char-secret
CORS_ORIGINS=http://localhost:3000
MCP_TOOLS_LOG_LEVEL=INFO
```

### Start Backend

```bash
uvicorn src.main:app --reload --port 8000
```

**✅ Success**: Visit http://localhost:8000/docs to see API docs.

---

## 🎨 Step 3: Frontend Setup (2 mins)

### Remove Old Dependency

```bash
cd frontend
npm uninstall @openai/chatkit-react
```

### Install Dependencies

```bash
npm install
```

### Start Frontend

```bash
npm run dev
```

**✅ Success**: Visit http://localhost:3000/dashboard/chat

---

## 🧪 Step 4: Test It! (1 min)

1. **Login** to your account (or signup)
2. **Navigate** to Dashboard → Chat
3. **Try these commands**:

```
You: "Add task buy groceries tomorrow"
AI: ✓ Created task: 'buy groceries' (ID: 1). Due: 2026-01-30.

You: "Mark it as done"
AI: ✓ Marked 'buy groceries' as complete. Great job! 🎉

You: "shw my tsks"  [typo on purpose]
AI: You have 0 task(s).
```

---

## ✅ What You Should See

### UI Features:
- ✅ Gradient rose-white background
- ✅ Seal-brown user message bubbles
- ✅ White AI message bubbles with border
- ✅ Bot and User icons
- ✅ Friendly welcome message

### AI Capabilities:
- ✅ **Memory**: "mark it complete" works (remembers "it")
- ✅ **Typo Handling**: "shw my tsks" → understands as "show my tasks"
- ✅ **Natural Language**: "What do I need to do?" works

---

## 🐛 Troubleshooting

### ❌ "Module not found: google-generativeai"

```bash
cd backend
pip install google-generativeai>=0.3.0
```

### ❌ "Gemini API unavailable"

Check `GEMINI_API_KEY` is set in `backend/.env`

### ❌ "Chat not loading"

1. Backend running? http://localhost:8000/docs
2. Token exists? Open DevTools → Application → Local Storage → `auth_token`

### ❌ "UI not matching theme"

Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

---

## 📈 What Changed?

| Component | Before | After |
|-----------|--------|-------|
| **Backend LLM** | OpenAI GPT-4o-mini | Gemini 1.5 Pro |
| **Cost** | $90-150/month | **$0** (free tier) |
| **Memory** | None | 10 messages |
| **Frontend UI** | OpenAI ChatKit | Custom shadcn/ui |
| **Theme** | Generic | Seal-brown/Rose-white |
| **Typo Handling** | Basic | Advanced |

---

## 🎯 Portfolio Features

Highlight these in your portfolio:

1. **AI Memory**: Context-aware conversations
2. **Error Tolerance**: Handles typos naturally
3. **Custom Design**: Built from scratch, theme-matched
4. **Zero Cost**: Production-ready with free tier
5. **Clean Architecture**: 4-agent system (Intent → Resolution → Action → Formatter)

---

## 📚 Full Documentation

For detailed documentation, see:
- `PHASE3_IMPLEMENTATION.md` - Complete setup guide
- `CLAUDE-PHASE3.md` - Architecture and constraints
- `specs/003-ai-chatbot/spec.md` - Feature requirements

---

## ✅ Verification Checklist

Before demo/deployment:

- [ ] Backend starts without errors
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Login/signup works
- [ ] Chat page loads
- [ ] Can create task via chat
- [ ] Memory works ("mark it complete")
- [ ] Typos are understood
- [ ] Task panel updates when tasks change
- [ ] Phase II functionality still works (tasks page)

---

## 🎉 You're Done!

Your AI chatbot is now:
- ✅ Running on Gemini (free tier)
- ✅ Context-aware (10-message memory)
- ✅ Typo-tolerant (friendly prompts)
- ✅ Theme-matched (seal-brown/rose-white)
- ✅ Production-ready

**Next**: Test thoroughly and deploy! 🚀
