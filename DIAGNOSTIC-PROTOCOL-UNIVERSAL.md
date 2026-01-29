# Universal Diagnostic Protocol
**For ALL Software Projects - Copy This to Every Repository**

---

## 🚨 MANDATORY: Read Before ANY Bug Fix

### The Golden Rule
> **"DIAGNOSE FIRST. FIX SECOND. NEVER GUESS."**

---

## 6-Step Diagnostic Protocol

### 1️⃣ REPRODUCE
- [ ] Can you reproduce the issue locally?
- [ ] What are the EXACT steps to reproduce?
- [ ] Does it happen in different browsers/environments?

**If NO, gather more info from user. If YES, continue.**

---

### 2️⃣ GATHER EVIDENCE (Use Browser DevTools)

**Check Console Errors:**
```javascript
// Look for ANY errors - they're usually the root cause
console.error logs? React errors? Network failures?
```

**Inspect the DOM:**
```javascript
const el = document.querySelector('[your-selector]');
console.log('Element exists?', el);
console.log('Styles:', window.getComputedStyle(el));
```

**For Click/Interaction Issues:**
```javascript
const el = document.querySelector('[your-selector]');
const rect = el.getBoundingClientRect();
const blocker = document.elementFromPoint(
  rect.left + rect.width/2,
  rect.top + rect.height/2
);
console.log('What is receiving clicks?', blocker);
console.log('Is it the expected element?', blocker === el);
console.log('Event handler exists?', el.onclick);
```

**For State/Render Issues:**
```javascript
// Check React DevTools
// Look for infinite loops: "Maximum update depth exceeded"
// Check component props and state
```

---

### 3️⃣ ISOLATE ROOT CAUSE

Ask these questions **IN ORDER**:

1. **Does the element exist in DOM?** → If NO: rendering issue
2. **Does it have correct attributes?** → If NO: implementation issue
3. **Is something blocking it?** → If YES: layout/CSS/z-index issue
4. **Are event handlers firing?** → If NO: JavaScript error
5. **Are there console errors?** → If YES: that's probably the root cause

**Stop asking questions when you find the issue.**

---

### 4️⃣ FORM HYPOTHESIS (With Evidence)

❌ **Bad:** "It's probably a framework bug"
❌ **Bad:** "Maybe it's a caching issue"
❌ **Bad:** "I think it's related to..."

✅ **Good:** "Console shows 'Maximum update depth' at line X. ElementFromPoint reveals SVG is blocking clicks. Hypothesis: Two issues - infinite loop + pointer-events."

**Hypothesis MUST be based on evidence, not guesses.**

---

### 5️⃣ TEST HYPOTHESIS

**Create minimal test case:**
```javascript
// Example: Test if pointer-events is the issue
element.style.pointerEvents = 'none';
// Click now - does it work?

// Example: Test if infinite loop is from specific useEffect
// Comment it out temporarily - does error disappear?
```

**If hypothesis is WRONG → Go back to Step 2**

**If hypothesis is RIGHT → Continue to Step 6**

---

### 6️⃣ IMPLEMENT FIX

Only after:
- ✅ Root cause confirmed with evidence
- ✅ Hypothesis tested successfully
- ✅ You understand WHY the fix works

**Implement ONE fix at a time. Test each fix.**

---

## 🚩 Red Flags (You're Doing It Wrong)

- 🚩 "Let me try this and see if it works" → You're guessing
- 🚩 "I found a similar issue on Stack Overflow" → You don't know YOUR issue
- 🚩 "The code looks correct to me" → You haven't tested it
- 🚩 "It's probably a [framework/library] bug" → You're making excuses
- 🚩 Implementing multiple changes at once → You don't know what works
- 🚩 Searching for solutions before understanding the problem → Wrong order

---

## ✅ Success Criteria

You did it right when:
- ✅ You can explain the root cause with evidence
- ✅ You reproduced the issue reliably
- ✅ You know WHY your fix works (not just that it works)
- ✅ Console has no errors after the fix
- ✅ User confirms it works in their environment

---

## 💾 Emergency Diagnostic Commands

### Navigation/Click Issues:
```javascript
// Find what's blocking clicks
const el = document.querySelector('[selector]');
const rect = el.getBoundingClientRect();
document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);

// Check event handlers
el.onclick
el.addEventListener('click', e => console.log('CLICKED', e), true);
```

### Layout/CSS Issues:
```javascript
const el = document.querySelector('[selector]');
const s = window.getComputedStyle(el);
console.log({
  display: s.display,
  position: s.position,
  zIndex: s.zIndex,
  pointerEvents: s.pointerEvents,
  visibility: s.visibility,
  opacity: s.opacity
});
```

### React State/Render Issues:
```javascript
// Check console for:
// "Maximum update depth exceeded" → Infinite loop
// "Cannot read property X of undefined" → Null reference
// "X is not a function" → Wrong type/missing import

// Use React DevTools to inspect:
// - Component props
// - Component state
// - Render count (if re-rendering constantly)
```

### Network/API Issues:
```javascript
// Check Network tab in DevTools
// Look for: 404, 500, CORS errors, slow requests

// Check if API is responding
fetch('/api/endpoint').then(r => r.json()).then(console.log)
```

---

## 📝 Before You Implement, Answer These:

- [ ] Have I checked the browser console for errors?
- [ ] Have I reproduced the issue locally?
- [ ] Have I inspected the DOM to verify elements exist?
- [ ] Have I used DevTools diagnostics (elementFromPoint, computed styles, etc.)?
- [ ] Have I tested my hypothesis with a minimal test?
- [ ] Do I understand WHY this fix will work?
- [ ] Am I fixing the ROOT CAUSE (not symptoms)?

**If ANY answer is NO → Do NOT implement. Go back and diagnose more.**

---

## 🎯 Real World Example (Learn From This)

**Issue:** Sidebar navigation icons not working

**❌ What I Did Wrong:**
1. Assumed duplicate routes were the issue → WRONG
2. Assumed z-index conflict → WRONG
3. Searched web for "Next.js Link not working" → WRONG
4. Applied "fixes" without diagnostics → WASTED TIME

**✅ What I Should Have Done:**
1. Asked user to run `document.elementFromPoint()` → Would reveal SVG blocking
2. Checked console errors immediately → Would reveal infinite loop
3. Fixed BOTH root causes based on evidence
4. Total time: 10 minutes instead of 45 minutes

**Lesson:** Evidence > Assumptions. Always.

---

## 🔄 Workflow Summary

```
BUG REPORTED
    ↓
1. REPRODUCE IT
    ↓
2. GATHER EVIDENCE (Browser DevTools)
    ↓
3. ISOLATE ROOT CAUSE (Ask systematic questions)
    ↓
4. FORM HYPOTHESIS (Based on evidence)
    ↓
5. TEST HYPOTHESIS (Minimal test case)
    ↓
6. IMPLEMENT FIX (One at a time)
    ↓
VERIFY & TEST
    ↓
✅ DONE
```

**Never skip steps. Never guess. Always diagnose.**

---

## 📋 Copy This To Every Project

**Recommended file name:** `DIAGNOSTIC-PROTOCOL.md` or `DEBUG-GUIDE.md`

**Add to your project templates:**
- Add reference in README.md
- Add reference in CONTRIBUTING.md
- Add reference in CLAUDE.md / AI instructions
- Train your team to follow this protocol

---

## 🎓 Final Wisdom

> **"A day of debugging can save you an hour of reading documentation."**
>
> Wait, that's backwards.
>
> **"An hour of proper diagnostics can save you a day of wrong fixes."**

**Diagnose thoroughly. Implement once. Ship quality.**

---

**Version:** 1.0
**Created:** 2026-01-28
**Origin:** Sidebar navigation debugging incident
**Purpose:** Prevent rushed implementations across ALL projects

**Apply this universally. Save time. Build better.**
