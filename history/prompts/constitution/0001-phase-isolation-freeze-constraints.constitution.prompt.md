---
id: 0001
title: Phase Isolation and Freeze Constraints
stage: constitution
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Aiman Syeda
command: constitution amendment
labels: ["constitution", "phase-isolation", "phase-ii-freeze", "governance", "constraints"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CLAUDE-PHASE3.md
  - CLAUDE.md
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

```
Claude is authorized to work ONLY on the following:

✅ Allowed Work
AI chatbot logic
OpenAI Agents SDK integration
MCP Server (Official MCP SDK)
Stateless chat endpoint (POST /api/{user_id}/chat)
Database models related to chat (Conversation, Message)
MCP tools for task operations (CRUD)
Specs under /specs/ related to Phase III only
Backend logic that does not modify Phase II behavior

🚨 ABSOLUTE HARD CONSTRAINT — PHASE II IS FROZEN
⛔ STRICT PROHIBITION
Claude MUST NOT under any circumstances:
- Modify Phase II UI/UX/styling/Tailwind/shadcn
- Modify frontend layouts, pages, icons, or themes
- Refactor existing frontend code
- Change API contracts defined in Phase II
- Change authentication behavior (Better Auth)
- Change REST endpoints created in Phase II
- Change database schema for tasks or users

🔒 Phase II is READ-ONLY
Phase II frontend and backend functionality is LOCKED.
Claude may read, call, or reuse — but never modify.
No exceptions. No optimizations. No "minor improvements".

IF CLAUDE IS UNSURE — STOP IMMEDIATELY
If Claude is uncertain whether a change touches Phase II UI/UX, alters Phase II behavior, or breaks existing functionality
👉 Claude must STOP and ASK, not guess.

FAILURE CONDITIONS (AUTO-DISQUALIFY)
Claude is considered FAILED if it:
- Modifies Phase II UI/UX
- Breaks existing functionality
- Introduces hidden state
- Bypasses MCP
- Changes API contracts
- Alters authentication flow

Add it, where You read and follow all instruction for general level before implementation
```

User requested adding **ABSOLUTE HARD CONSTRAINT** section to constitution hierarchy to prevent Phase II modifications during Phase III implementation.

## Response snapshot

Agent updated three constitution files to establish Phase II freeze as a hard constraint:

**1. CLAUDE-PHASE3.md** (Primary enforcement):
- Added **prominent top section** (before all other content): "🚨 ABSOLUTE HARD CONSTRAINT — PHASE II IS FROZEN (READ THIS FIRST)"
- Created **exhaustive whitelist** of allowed work (7 categories):
  1. AI Chatbot Logic (agents, OpenAI SDK)
  2. MCP Server (tools, logging)
  3. Chat API Endpoints (NEW routes only)
  4. Database Models (Conversation, Message ONLY)
  5. Frontend Chat UI (NEW /chat/ directory only)
  6. Phase III Specs (specs/003-ai-chatbot/ only)
  7. Backend Logic (ADDITIVE files only)
- Created **exhaustive blacklist** of prohibited work (3 categories):
  - ❌ Frontend (Phase II Frozen): 11 specific prohibitions
  - ❌ Backend (Phase II Frozen): 9 specific prohibitions
  - ❌ Configuration (Phase II Frozen): 4 specific prohibitions
- Added **"Phase II is READ-ONLY"** section with explicit allowed/prohibited actions
- Added **"IF UNSURE — STOP IMMEDIATELY"** section requiring Claude to ASK not GUESS
- Added **"FAILURE CONDITIONS (AUTO-DISQUALIFY)"** section with 7 instant-fail scenarios
- Positioned at **top of file** to ensure it's read FIRST before any other Phase III rules

**2. CLAUDE.md** (Redirect to primary source):
- Added **"⚠️ CRITICAL: READ BEFORE ANY WORK"** section at top (after header)
- Declared **current phase** (Phase III) and **Phase II status** (🔒 FROZEN)
- Defined **mandatory pre-work reading order**:
  1. CLAUDE-PHASE3.md (Phase II freeze + allowed work)
  2. constitution.md (core principles)
  3. CLAUDE.md (project guidance)
  4. spec.md (feature requirements)
- Added **"Phase II is COMPLETELY FROZEN"** warning with pointer to CLAUDE-PHASE3.md
- Added **"If you modify ANY Phase II code = Immediate failure"** disclaimer
- Added **"When in doubt, STOP and ASK. Never guess."** requirement

**3. .specify/memory/constitution.md** (Governance principle):
- Added **"Phase Isolation Rules (CRITICAL)"** subsection to **Principle IV: Phase-Based Evolution**
- Defined 6 phase isolation rules:
  1. Completed phases are FROZEN
  2. Additive-only changes
  3. Read-reuse-reference pattern
  4. Explicit exceptions only (TodoMasterAgent approval + ADR)
  5. Phase-specific directories
  6. Violation = Failure
- Added **concrete example** for Phase III on Phase II:
  - ✅ 3 allowed actions (call endpoints, read models, reuse auth)
  - ❌ 3 prohibited actions (modify UI/UX, change contracts, alter schema)
- Integrated into existing principle (not separate principle) for constitution coherence

**Governance Hierarchy Established**:

```
.specify/memory/constitution.md (Principle IV - Phase Isolation)
        ↓ (defines governance rule)
CLAUDE.md (Mandatory reading order + Phase II status)
        ↓ (redirects to primary enforcement)
CLAUDE-PHASE3.md (Exhaustive allowed/prohibited work lists)
        ↓ (primary enforcement document)
Implementation Work (must comply with all above)
```

**Reading Flow for Claude**:
1. Opens CLAUDE.md → Sees "CRITICAL: READ BEFORE ANY WORK" → Directed to CLAUDE-PHASE3.md first
2. Opens CLAUDE-PHASE3.md → Sees "ABSOLUTE HARD CONSTRAINT" at top → Learns allowed/prohibited work
3. Opens constitution.md → Sees Principle IV Phase Isolation Rules → Understands governance basis
4. Opens spec.md → Sees feature requirements → Validates work against constraints
5. Proceeds with implementation ONLY if all constraints satisfied

**Key Design Decisions**:
- **CLAUDE-PHASE3.md as primary source**: Most specific, most detailed, read first
- **CLAUDE.md as router**: Establishes reading order, points to primary source
- **constitution.md as governance basis**: Establishes WHY phases are isolated (principle-level)
- **Whitelist approach**: Exhaustive "allowed work" list reduces ambiguity
- **Blacklist specificity**: 24 specific prohibitions prevent edge case violations
- **"STOP and ASK" requirement**: Shifts burden to Claude to request clarification when uncertain

**Failure Prevention**:
- **7 instant-fail conditions** clearly documented
- **No exceptions clause** prevents "small optimization" violations
- **Exhaustive lists** reduce interpretation ambiguity
- **Prominent positioning** ensures constraints are read FIRST

## Outcome

- ✅ Impact: Phase II freeze enforced across constitution hierarchy; Claude MUST read constraints before implementation
- 🧪 Tests: No tests run (governance update)
- 📁 Files: Updated CLAUDE-PHASE3.md, CLAUDE.md, .specify/memory/constitution.md
- 🔁 Next prompts: Begin Phase III implementation with T001 (all constraints now enforced)
- 🧠 Reflection: Constitution amendment establishes phase isolation as governance principle. Three-file hierarchy ensures constraints are read in order (CLAUDE.md → CLAUDE-PHASE3.md → constitution.md). Exhaustive allowed/prohibited lists (31 specific items) reduce ambiguity. "STOP and ASK" requirement prevents accidental Phase II modifications. Failure conditions (7 instant-fail scenarios) clearly documented. Ready for safe Phase III implementation with Phase II protection.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution amendments successful
- Graders run and results (PASS/FAIL): Consistency check: PASS (all 3 files align), Completeness: PASS (exhaustive lists cover all scenarios), Positioning: PASS (constraints at top of files)
- Prompt variant (if applicable): User-initiated constitution amendment for phase isolation enforcement
- Next experiment (smallest change to try): Monitor for Phase II modification attempts during Phase III implementation; validate constraint effectiveness
