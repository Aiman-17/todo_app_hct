# CLAUDE.md Diagnostic Snippet
**Copy this to the TOP of CLAUDE.md in EVERY project**

---

```markdown
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

### Real Example (Learn From This):
**Issue:** Navigation not working

**❌ Wrong approach:** Assumed routes/z-index/framework bug → Wasted 45 mins

**✅ Right approach:**
1. User runs `document.elementFromPoint()` → SVG blocking clicks
2. Check console → Infinite loop error
3. Fix both → 10 minutes

**Evidence > Assumptions. Always.**

---

**Workflow:** REPRODUCE → GATHER EVIDENCE → ISOLATE CAUSE → TEST HYPOTHESIS → FIX

**Never skip steps. Never guess. Always diagnose.**
```

---

## How to Use:

1. Copy the markdown block above (lines 7-91)
2. Paste at the TOP of CLAUDE.md in EVERY project
3. Place it BEFORE any project-specific instructions

This ensures diagnostic protocol is the first thing any AI reads before working on bugs.
