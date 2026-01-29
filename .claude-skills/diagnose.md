# Diagnose Bug - Interactive Diagnostic Protocol

**Command:** `/diagnose`

**Description:** Guides you through systematic bug diagnosis before implementing any fix. Enforces evidence-gathering and prevents rushed implementations.

---

## Skill Behavior

When user runs `/diagnose [bug description]`:

### Phase 1: Evidence Gathering (Mandatory)

**Ask the user these questions sequentially:**

1. **"What is the exact bug behavior you're seeing?"**
   - Get specific steps to reproduce
   - Confirm environment (local/production, browser)

2. **"Have you checked the browser console for errors?"**
   - If NO → STOP. Ask them to check console first and report back
   - If YES → Ask them to paste the errors

3. **"Can you reproduce this locally?"**
   - If NO → Ask for more details about environment differences
   - If YES → Continue

4. **For Click/Interaction Issues:**
   ```javascript
   // Ask user to run this and report output:
   const el = document.querySelector('[selector-for-broken-element]');
   const rect = el.getBoundingClientRect();
   const blocker = document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);
   console.log('Element receiving click:', blocker);
   console.log('Expected element:', el);
   console.log('Match?', blocker === el);
   ```

5. **For Layout/Style Issues:**
   ```javascript
   // Ask user to run this:
   const el = document.querySelector('[selector]');
   const s = window.getComputedStyle(el);
   console.log({
     display: s.display,
     position: s.position,
     zIndex: s.zIndex,
     pointerEvents: s.pointerEvents,
     visibility: s.visibility
   });
   ```

### Phase 2: Root Cause Analysis

Based on evidence gathered:

1. **Identify the root cause with evidence**
   - Example: "Console shows 'Maximum update depth exceeded' at FilterContext.tsx:118"
   - Example: "elementFromPoint returns <svg>, not <a> - SVG blocking clicks"

2. **Form hypothesis**
   - Must be based on evidence, not assumptions
   - Example: "Hypothesis: SVG icons have default pointer-events, blocking Link clicks"

3. **Present hypothesis to user**
   - "Based on evidence, the root cause is: [X]"
   - "This explains the bug because: [Y]"
   - "To confirm, let's test: [Z]"

### Phase 3: Hypothesis Testing

**Before implementing ANY fix:**

1. **Propose a minimal test**
   ```javascript
   // Example: Test if pointer-events is the issue
   element.style.pointerEvents = 'none';
   // Ask user: "Now click - does it work?"
   ```

2. **Get user confirmation**
   - "Did the test confirm the hypothesis?"
   - If NO → Go back to Phase 2
   - If YES → Proceed to Phase 4

### Phase 4: Implementation

**Only now can you implement the fix:**

1. Show the proposed fix
2. Explain WHY it works
3. Implement the fix
4. Ask user to verify in their environment

---

## Red Flags (Skill Should Warn About)

If you catch yourself doing any of these, STOP and restart diagnosis:

- 🚩 "Let me try this fix and see" → You're guessing
- 🚩 "I found a similar issue online" → You don't know YOUR issue
- 🚩 "It's probably a [framework] bug" → You're making excuses
- 🚩 Implementing without user running diagnostics → No evidence
- 🚩 Skipping hypothesis testing → Unconfirmed fix

---

## Example Flow

```
User: /diagnose Navigation icons not working in sidebar
Assistant: Let me gather evidence first.

**Phase 1: Evidence Gathering**

1. What is the exact behavior?
   User: When I click Calendar/Chat/Settings icons, nothing happens

2. Have you checked console for errors?
   User: Yes - "Maximum update depth exceeded" in FilterContext.tsx:118

3. Can you reproduce locally?
   User: Yes

4. Please run this diagnostic and share output:
   ```javascript
   const link = document.querySelector("aside a");
   const rect = link.getBoundingClientRect();
   const blocker = document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);
   console.log("Blocker:", blocker, "Expected:", link, "Match:", blocker === link);
   ```

User: Output shows blocker is <svg>, not <a>. Match: false

**Phase 2: Root Cause Analysis**

Evidence gathered:
1. Console error: Infinite loop in FilterContext
2. elementFromPoint: SVG blocking clicks

Root causes identified:
1. FilterContext setters not wrapped in useCallback → infinite re-renders
2. SVG icons intercepting click events before reaching Link

**Phase 3: Hypothesis Testing**

Test 1: "Run element.style.pointerEvents = \"none\" on SVG. Does clicking work now?"
User: No, still doesnt work

Test 2: "The infinite loop is crashing the app. Thats blocking ALL navigation."
User: Console shows constant re-renders, yes

**Phase 4: Implementation**

Fix 1: Wrap FilterContext setters in useCallback
Fix 2: Add pointer-events-none to SVG icons

*Implements both fixes*

Result: Navigation works! ✅
```

---

## Success Criteria

This skill succeeds when:
- ✅ Evidence is gathered BEFORE any fix
- ✅ Root cause is identified with proof
- ✅ Hypothesis is tested minimally
- ✅ User confirms the fix works
- ✅ You can explain WHY it works

---

**Rule: "Evidence > Assumptions. Always."**

