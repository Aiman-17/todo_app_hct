# How to Apply Diagnostic Protocol to All Projects

## Quick Start (3 Minutes Per Project)

### For Existing Projects:

1. **Open CLAUDE.md** (or create it if it doesn't exist)

2. **Add this at the TOP** (before any other instructions):

```bash
# Copy from line 7 to line 91 of CLAUDE-DIAGNOSTIC-SNIPPET.md
# Paste at the very top of your CLAUDE.md
```

3. **Save and commit:**
```bash
git add CLAUDE.md
git commit -m "docs: add diagnostic protocol for bug fixes"
git push
```

**Done!** This project now has the diagnostic protocol.

---

## For New Projects:

### Method 1: Use the Template (Recommended)

```bash
# When creating a new project:
cp ~/path/to/CLAUDE-TEMPLATE-WITH-DIAGNOSTICS.md ./CLAUDE.md

# Edit the "Project-Specific Instructions" section
# Add your tech stack, guidelines, etc.

# Commit
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with diagnostic protocol"
```

### Method 2: Create Your Own Template

1. Copy `CLAUDE-TEMPLATE-WITH-DIAGNOSTICS.md`
2. Customize it with your preferred defaults
3. Save as `~/project-templates/CLAUDE-BASE.md`
4. Use it for all new projects

---

## Files You Created (Reference):

### 1. **DIAGNOSTIC-PROTOCOL-UNIVERSAL.md**
- **Purpose:** Comprehensive guide (standalone)
- **Use:** For deep understanding, reference, training
- **Copy to:** Projects that need full documentation

### 2. **CLAUDE-DIAGNOSTIC-SNIPPET.md**
- **Purpose:** Quick copy-paste snippet for CLAUDE.md
- **Use:** Add to CLAUDE.md in all projects
- **Copy to:** Every project's CLAUDE.md (top section)

### 3. **CLAUDE-TEMPLATE-WITH-DIAGNOSTICS.md**
- **Purpose:** Complete CLAUDE.md template with diagnostics built-in
- **Use:** Starting point for new projects
- **Copy to:** New projects as their initial CLAUDE.md

---

## Verification Checklist

After adding to a project, verify:

- [ ] Diagnostic protocol is at the TOP of CLAUDE.md
- [ ] The golden rule is visible: "DIAGNOSE FIRST. FIX SECOND. NEVER GUESS."
- [ ] Browser diagnostic commands are included
- [ ] Red flags section is present
- [ ] Checklist is included

---

## Quick Copy-Paste for Existing CLAUDE.md Files

**Open your existing CLAUDE.md and add this section at the top:**

```markdown
## 🚨 CRITICAL: Diagnostic Protocol (READ BEFORE ANY BUG FIX)

### The Golden Rule
> **"DIAGNOSE FIRST. FIX SECOND. NEVER GUESS."**

### Before ANY bug fix:
1. ✅ Check browser console for errors FIRST
2. ✅ Use DevTools diagnostics (elementFromPoint, computed styles)
3. ✅ Gather evidence - don't assume
4. ✅ Test hypothesis with minimal test
5. ✅ Understand WHY fix works before implementing

### Quick Diagnostics:
```javascript
// Find what's blocking clicks:
const el = document.querySelector('[selector]');
const rect = el.getBoundingClientRect();
const blocker = document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);
console.log('Blocker:', blocker, 'Expected:', el, 'Match:', blocker === el);
```

**Never guess. Always diagnose. Evidence > Assumptions.**

---
```

**Then save and commit.**

---

## Pro Tip: Add to Your AI Tool Config

If you use Cursor, Windsurf, Cline, or similar tools:

1. Find their config file (`.cursorrules`, `.clinerules`, etc.)
2. Add the diagnostic snippet there too
3. Now ALL AI interactions in that project follow the protocol

---

## Team Onboarding

To train your team:

1. **README.md:** Add link to diagnostic protocol
```markdown
## Debugging
Before fixing bugs, read [DIAGNOSTIC-PROTOCOL-UNIVERSAL.md](./DIAGNOSTIC-PROTOCOL-UNIVERSAL.md)
```

2. **CONTRIBUTING.md:** Add to the workflow
```markdown
### Bug Fix Workflow
1. Read DIAGNOSTIC-PROTOCOL-UNIVERSAL.md
2. Follow the 6-step process
3. Include evidence in your PR description
```

3. **PR Template:** Add diagnostic checklist
```markdown
## Bug Fix Checklist
- [ ] Checked browser console for errors
- [ ] Used DevTools to gather evidence
- [ ] Tested hypothesis before implementing
- [ ] Can explain WHY this fix works
```

---

## Maintenance

**Once a year, review and update:**
- Add new diagnostic commands you discovered
- Add examples from real bugs you fixed
- Update for new frameworks/tools you're using

---

## Success Metrics

You know it's working when:
- ✅ Bug fixes have evidence in PR descriptions
- ✅ "I tried this randomly" stops happening
- ✅ Debugging time decreases
- ✅ Fewer wrong fixes are implemented
- ✅ Team can explain WHY fixes work

---

## Summary

**3 files. 3 use cases:**

1. **DIAGNOSTIC-PROTOCOL-UNIVERSAL.md** → Full guide (standalone)
2. **CLAUDE-DIAGNOSTIC-SNIPPET.md** → Copy to CLAUDE.md (all projects)
3. **CLAUDE-TEMPLATE-WITH-DIAGNOSTICS.md** → Template for new projects

**Total time to apply:** 3 minutes per project

**Time saved per bug:** 15-45 minutes (based on today's experience)

**ROI:** Massive. Do it now.

---

**Start with your most active projects. Apply to all within a week. Make it standard.**
