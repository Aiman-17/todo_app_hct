# Critical Diagnostic Principles

**MANDATORY: Read this before implementing ANY fix**

## The Mistake That Was Made (2026-01-28)

### What Happened:
A sidebar navigation issue was reported. Instead of diagnosing, I:
1. ❌ Assumed it was a duplicate route issue → **WRONG**
2. ❌ Assumed it was a z-index conflict → **WRONG**
3. ❌ Web searched and assumed Next.js 15 production bug → **WRONG**
4. ❌ Applied fixes without understanding root cause → **WASTED TIME**

### The Real Issues (found ONLY after proper diagnostics):
1. ✅ SVG icons blocking clicks (`document.elementFromPoint` revealed it)
2. ✅ Infinite loop crashing the app (console errors showed it)

**Time wasted: ~45 minutes. Could have been solved in 10 minutes with proper diagnostics.**

---

## MANDATORY Diagnostic Protocol

### 🚨 BEFORE ANY FIX: DIAGNOSE FIRST

**"STOP. THINK. DIAGNOSE. THEN FIX."**

### Step 1: GATHER EVIDENCE (Don't Guess!)

When a bug is reported, immediately collect:

```javascript
// 1. Check console errors
console.log('Any errors in browser console?')

// 2. Inspect the DOM
const element = document.querySelector('[target-selector]');
console.log('Element exists?', element);
console.log('Computed styles:', window.getComputedStyle(element));

// 3. Check what's blocking clicks
const rect = element.getBoundingClientRect();
const blocker = document.elementFromPoint(
  rect.left + rect.width/2,
  rect.top + rect.height/2
);
console.log('What element is receiving clicks?', blocker);
console.log('Is it the expected element?', blocker === element);

// 4. Check event handlers
console.log('Event handler exists?', element.onclick);
```

**DO NOT implement anything until you have data.**

### Step 2: REPRODUCE THE ISSUE

- ✅ Test in local environment
- ✅ Test in production (if different)
- ✅ Check browser console for errors
- ✅ Use DevTools Inspector
- ✅ Try different browsers if needed

**If you cannot reproduce it, you cannot fix it.**

### Step 3: ISOLATE THE ROOT CAUSE

Ask these questions IN ORDER:

1. **Does the element exist in the DOM?**
   - If NO → rendering issue
   - If YES → continue

2. **Does the element have the correct attributes?**
   - Check href, onClick, event handlers
   - If NO → implementation issue
   - If YES → continue

3. **Is something blocking the element?**
   - Use `document.elementFromPoint(x, y)`
   - Check z-index stacking context
   - Check pointer-events CSS
   - If YES → layout/CSS issue
   - If NO → continue

4. **Are event handlers firing?**
   - Add temporary event listener to test
   - Check `event.defaultPrevented`
   - If NO → JavaScript error preventing handlers
   - If YES → continue

5. **Is there a runtime error preventing navigation?**
   - Check console for errors
   - Check for infinite loops
   - Check for state management issues

### Step 4: FORM A HYPOTHESIS

Only AFTER gathering evidence, form a hypothesis:

**Good hypothesis:**
> "Based on `document.elementFromPoint()` showing `<polyline>`, the SVG icon is blocking clicks. The console shows 'Maximum update depth exceeded' causing app crashes."

**Bad hypothesis (what I did):**
> "It's probably a Next.js 15 bug I read about online."

### Step 5: TEST THE HYPOTHESIS

Create a minimal test:

```javascript
// Quick test for click blocking
element.style.pointerEvents = 'none';
// Now click - does it work?

// Quick test for infinite loop
// Check if specific useEffect is causing it
// Comment out temporarily and verify
```

**If hypothesis is wrong, go back to Step 1. DO NOT implement a fix.**

### Step 6: IMPLEMENT THE FIX

Only implement after:
- ✅ Root cause confirmed
- ✅ Hypothesis tested
- ✅ Solution verified locally

---

## Red Flags: When You're Doing It WRONG

🚩 **"It's probably a [framework] bug"** → You're guessing
🚩 **"Let me try changing this and see"** → You're randomly fixing
🚩 **"I'll apply this fix from Stack Overflow"** → You don't understand the issue
🚩 **"The code looks correct, so..."** → You haven't tested it
🚩 **"Let me implement multiple fixes at once"** → You don't know which one works

---

## Critical Thinking Checklist

Before implementing ANY fix, answer these:

- [ ] Have I reproduced the issue myself?
- [ ] Have I checked the browser console for errors?
- [ ] Have I inspected the DOM to verify the element exists?
- [ ] Have I used browser DevTools to check what's blocking clicks?
- [ ] Have I tested my hypothesis with a minimal test case?
- [ ] Do I understand WHY this fix will work?
- [ ] Have I verified there are no other root causes?

**If you answered NO to any of these, DO NOT IMPLEMENT A FIX.**

---

## The Right Mindset

### ❌ Wrong Approach:
"The user says navigation doesn't work. Let me check the routes... they look fine. Maybe it's a Next.js bug. Let me search for similar issues... found one! Let me apply that fix."

### ✅ Right Approach:
"The user says navigation doesn't work. Let me ask them to run diagnostics in the browser console to see what's actually happening. The console shows SVG elements are blocking clicks AND there's an infinite loop error. Let me verify both issues locally, then fix them in order."

---

## Lessons from This Issue

### What I Should Have Done:

1. **IMMEDIATELY ask user to run browser diagnostics:**
   ```javascript
   document.querySelectorAll('aside a').length // Links exist?
   document.elementFromPoint(x, y) // What's blocking?
   ```

2. **CHECK CONSOLE ERRORS first** - would have seen infinite loop immediately

3. **TEST HYPOTHESIS before implementing** - could have asked user to test pointer-events in console

4. **ONE FIX AT A TIME** - not jump from duplicate routes → z-index → Next.js bug

### What I Did Wrong:

1. ❌ Jumped to implementation without diagnostics
2. ❌ Made assumptions based on code review alone
3. ❌ Applied multiple "fixes" that weren't fixing the real issue
4. ❌ Relied on web search instead of actual debugging
5. ❌ Didn't listen when user said "right-click works" (huge clue!)

---

## Emergency Diagnostic Commands

Keep these ready for common issues:

### Navigation Not Working:
```javascript
// What element is actually being clicked?
const link = document.querySelector('[your-selector]');
const rect = link.getBoundingClientRect();
document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);

// Are event handlers attached?
link.onclick

// Does clicking actually trigger?
link.addEventListener('click', e => console.log('CLICKED!', e));
```

### Infinite Loops:
```javascript
// Check console for "Maximum update depth exceeded"
// Check which file/line is triggering it
// Look for useEffect without proper dependencies
```

### CSS/Layout Issues:
```javascript
const el = document.querySelector('[selector]');
const styles = window.getComputedStyle(el);
console.log({
  display: styles.display,
  position: styles.position,
  zIndex: styles.zIndex,
  pointerEvents: styles.pointerEvents
});
```

---

## Final Rule

> **"Measure twice, cut once."**
>
> In debugging: **"Diagnose thoroughly, implement once."**

**DO NOT SKIP DIAGNOSTICS. EVER.**

---

## Success Criteria

You've done it right when:
- ✅ You can explain the root cause with evidence
- ✅ You can reproduce the issue reliably
- ✅ You know WHY your fix works
- ✅ You tested the fix before committing
- ✅ The user confirms it works

---

**This document was created after wasting time on wrong solutions.**
**Read it. Follow it. Save time. Ship quality.**

Created: 2026-01-28
Issue: Sidebar navigation routing failure
Root causes: SVG pointer-events + FilterContext infinite loop
Time wasted: ~45 minutes due to poor diagnostic approach
