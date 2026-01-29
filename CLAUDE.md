# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

---

## 🚨 BEFORE ANY BUG FIX: RUN `/diagnose`

**Rule: "Evidence > Assumptions. Always."**

### Mandatory Protocol:
1. ✅ Check browser console for errors (90% of root causes)
2. ✅ Use `document.elementFromPoint(x, y)` for click issues
3. ✅ Test hypothesis before implementing
4. ✅ Understand WHY the fix works

**Use `/diagnose [bug description]` to follow the systematic diagnostic protocol.**

🛠️ Skill: [.claude-skills/diagnose.md](./.claude-skills/diagnose.md)

---

## ⚠️ CRITICAL: READ BEFORE ANY WORK

**Current Phase**: Phase III - AI Chatbot Interface
**Phase II Status**: 🔒 **FROZEN** - Completely read-only

### 🚨 MANDATORY PRE-WORK READING ORDER

Before starting **ANY** implementation work, you **MUST** read in this exact order:

```
1. CLAUDE-PHASE3.md → Phase II freeze constraints + allowed work
   ↓
2. .specify/memory/constitution.md → Core principles + agent governance
   ↓
3. CLAUDE.md (this file) → Project-level guidance
   ↓
4. specs/003-ai-chatbot/spec.md → Feature requirements
```

### 🔒 Phase II is COMPLETELY FROZEN

**You are ONLY authorized to work on Phase III AI Chatbot components.**

See `CLAUDE-PHASE3.md` (top section: "ABSOLUTE HARD CONSTRAINT") for:
- ✅ Exhaustive list of allowed work
- ❌ Strict prohibitions (Phase II modifications)
- 💀 Failure conditions (instant disqualification)

**If you modify ANY Phase II code = Immediate failure. No exceptions.**

👉 **When in doubt, STOP and ASK. Never guess.**

---

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.






# CLAUDE OPERATION CONSTITUTION

## Execution Environment Constraints

You are operating in a Windows environment with Git Bash and PowerShell.
This environment DOES NOT support reliable Bash heredocs or complex shell
string quoting.

### STRICT PROHIBITIONS (NON-NEGOTIABLE)

You MUST NOT:
- Use Bash heredocs (<< EOF, << 'EOF', etc.)
- Use multi-line strings inside bash -c or python -c
- Attempt to write large specification files via shell commands
- Use triple-quoted strings inside shell invocations
- Mix PowerShell and Bash in the same operation
- Retry shell-based file writes after a failure

If a task requires writing long-form content (specs, constitution, README,
markdown documentation), you MUST output the content as a Markdown code block
ONLY and ask the user to manually paste it into the file.

Violation of these rules is considered a critical execution failure.

---

## Allowed File Writing Rules

You MAY:
- Use the Write tool for direct file creation when available
- Use shell commands ONLY for:
  - Creating directories
  - Creating empty files
  - Running Python scripts that already exist
- Write short code snippets (<30 lines) via shell when safe

You MUST:
- Prefer content generation over file manipulation
- Prefer manual paste instructions for long documents

---

## Spec-Kit + Hackathon Workflow Rules

This project uses Spec-Kit Plus and spec-driven development.

You MUST:
- Generate specifications BEFORE implementation
- Never assume a spec exists unless confirmed
- Never bypass the spec phase
- Follow phased delivery:
  Phase 0: Constitution
  Phase 1: In-Memory Console App
  Phase 2: Persistence
  Phase 3: Enhancements (if applicable)

Each phase MUST be completed and validated before moving forward.

---

## Failure Handling Protocol

If any shell or file operation fails:
1. STOP immediately
2. Do NOT retry with alternative shell tricks
3. Explain the failure clearly
4. Switch to content-only output mode

---

## Quality Bar

This is a hackathon submission.
Code must be:
- Clean
- Minimal
- Deterministic
- Free of experimental patterns

Documentation must be:
- Copy-paste ready
- Deterministic
- Explicit

Assume evaluators will review commit history and spec quality.

## Active Technologies
- Python 3.13+ (backend), TypeScript 5+ with strict mode (frontend) + FastAPI, Uvicorn, SQLModel, Better Auth (backend); Next.js 16+, React 19+, shadcn/ui, Better Auth (frontend) (002-fullstack-web-auth)
- Neon Serverless PostgreSQL with connection pooling (002-fullstack-web-auth)
- OpenAI Agents SDK, MCP (Model Context Protocol) SDK, OpenAI ChatKit (frontend) (003-ai-chatbot)

## Recent Changes
- 003-ai-chatbot: Added OpenAI Agents SDK for conversational AI, MCP SDK for tool orchestration, OpenAI ChatKit for frontend chat UI
- 002-fullstack-web-auth: Added Python 3.13+ (backend), TypeScript 5+ with strict mode (frontend) + FastAPI, Uvicorn, SQLModel, Better Auth (backend); Next.js 16+, React 19+, shadcn/ui, Better Auth (frontend)

