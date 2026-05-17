---
name: session-summary
description: This skill should be used when the user asks to "session summary", "summarize session", "总结会话", "会话总结", "写总结", "收尾", or invokes /session-summary. Writes TWO files to ~/.agent/: an experience-xxx.md (pitfalls, error corrections, tool/subagent efficiency) and a record-xxx.md (objective work progress, current status). Manual trigger only — not automatic.
---

# Session Summary

Write two structured files summarizing the current session: one for lessons learned, one for work progress.

This is a **manual** skill — trigger only on explicit user request. Do not run automatically.

## Workflow

### Step 1 — Review Session

Scan the current conversation for:

**For `experience-xxx.md`:**
- Errors encountered and how they were fixed
- Pitfalls, dead ends, wrong assumptions
- Tool / subagent usage patterns that worked or failed
- Efficiency observations (what was slow, what was fast)
- Cross-file verification failures (agent claimed success but VCS diff empty, etc.)

**For `record-xxx.md`:**
- What objective work was done (files changed, commits made, configs updated)
- Current state of each workstream
- What is complete vs what remains
- Key decisions with rationale

### Step 2 — Choose Topic Slug

Derive a short topic slug from the session's main work. Use lowercase, hyphens.

Good: `openclaw-config-inventory-and-fixes`, `cc-skill-session-summary`
Bad: `stuff`, `session`, `misc`

### Step 3 — Check for Overlap

Scan `~/.agent/` for existing files on the same topic:

```bash
ls ~/.agent/experience-*.md ~/.agent/record-*.md 2>/dev/null
```

If files on the same topic exist, ask: "和 `xxx.md` 有重叠，合并还是新建？"

### Step 4 — Confirm Filenames

Propose both filenames to the user:

```
experience-<topic>.md
record-<topic>.md
```

Wait for confirmation. User reply '1' means confirmation.

### Step 5 — Write experience-xxx.md

Structure:

```markdown
# experience-<topic>

Context: <1-2 lines describing what this session was about>

## 踩坑与发现

### 1. <pitfall title>

**现象**: <what went wrong>
**原因**: <root cause>
**解决**: <how fixed>
**教训**: <what to do differently next time>

### 2. <next pitfall>
...

## 高效工作流总结

1. <pattern>: <why it worked>
2. <pattern>: <why it worked>
```

Focus on **reusable lessons**, not session narrative. Each pitfall should be actionable for future sessions.

### Step 6 — Write record-xxx.md

Structure:

```markdown
# record-<topic>

Context: <date and 1-line summary>

## 工作过程

### 1. <workstream title>

<what was done, with file paths and key details>

### 2. <next workstream>
...

## 当前状态

- <status bullet 1>
- <status bullet 2>
- 待补充: <remaining items>
```

Focus on **objective facts** — what files changed, what state things are in, what's left.

### Step 7 — Git Commit

```bash
cd ~/.agent && git add -A && git commit -m "session-summary: <topic>"
```

If commit fails (not a git repo), run `git init` and retry.
If the commit is purely a rename of the previous commit's file, use `--amend` instead of a new commit.

### Step 8 — Post-Write Check

If root-level `.md` files in `~/.agent/` exceed 20, invoke `/sort`.

## Content Guidelines

- **One session = one pair of files.** If the session spanned multiple topics, pick the dominant one for filenames and cover subtopics within.
- Same language as user's input.
- **experience**: focus on **why** (rationale has more replay value than facts). Include exact error messages, commands, file paths.
- **record**: focus on **what** (objective state, not interpretation). Like `/export` — concrete, verifiable.
- Be concise. No fluff, no repetition.
- If appending to existing files, read first, then edit.

## Quick Reference

| File | Purpose | Question Answered |
|------|---------|-------------------|
| `experience-xxx.md` | Pitfalls, corrections, efficiency | "What did I learn that I should not repeat?" |
| `record-xxx.md` | Work progress, current status | "What did I actually do and what's left?" |
