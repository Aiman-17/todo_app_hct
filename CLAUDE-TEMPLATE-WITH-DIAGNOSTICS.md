# Claude Code Rules

**COPY THIS TEMPLATE TO ALL NEW PROJECTS**

---

## 🚨 CRITICAL: Diagnostic Protocol (READ BEFORE ANY BUG FIX)

### The Golden Rule
> **"DIAGNOSE FIRST. FIX SECOND. NEVER GUESS."**

### Mandatory Steps Before ANY Bug Fix:

#### 1. CHECK CONSOLE ERRORS FIRST
```javascript
// Look in browser DevTools console
// React errors? Network failures? JavaScript errors?
// These are usually the root cause
```

#### 2. GATHER EVIDENCE (Don't Assume!)
```javascript
// For click/interaction issues:
const el = document.querySelector('[your-selector]');
const rect = el.getBoundingClientRect();
const blocker = document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);
console.log('What element is receiving clicks?', blocker);
console.log('Is it the expected element?', blocker === el);

// For layout issues:
const styles = window.getComputedStyle(el);
console.log({ display, position, zIndex, pointerEvents } = styles);
```

#### 3. ISOLATE ROOT CAUSE
Ask systematically:
- Does element exist in DOM?
- Does it have correct attributes?
- Is something blocking it?
- Are event handlers attached?
- Are there console errors?

#### 4. TEST HYPOTHESIS
```javascript
// Example: Test if pointer-events is the issue
element.style.pointerEvents = 'none';
// Now click - does it work?
```

#### 5. IMPLEMENT (Only After Diagnosis)
- ✅ Root cause confirmed with evidence
- ✅ Hypothesis tested
- ✅ You understand WHY the fix works

### 🚩 Red Flags (You're Doing It Wrong)
- 🚩 "Let me try this and see" → You're guessing
- 🚩 "I found a similar issue online" → You don't know YOUR issue
- 🚩 "It's probably a [framework] bug" → You're making excuses
- 🚩 Implementing multiple changes at once → You don't know what works
- 🚩 Searching solutions before understanding problem → Wrong order

### ✅ Checklist Before Implementation:
- [ ] Checked browser console for errors?
- [ ] Reproduced issue locally?
- [ ] Used DevTools diagnostics (elementFromPoint, computed styles)?
- [ ] Tested hypothesis with minimal test case?
- [ ] Understand WHY this fix works (not just that it works)?

**If ANY answer is NO → STOP. Diagnose more. Do NOT implement.**

---

## Project-Specific Instructions

[Your project-specific instructions go here]

### Tech Stack
- Framework: [e.g., Next.js, React, Vue]
- Backend: [e.g., FastAPI, Express, Django]
- Database: [e.g., PostgreSQL, MongoDB]

### Development Guidelines
[Your specific coding standards, patterns, etc.]

### Task Management
[Your workflow instructions]

---

**Remember:** Evidence > Assumptions. Always diagnose before implementing.
