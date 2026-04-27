---
name: persist
description: This skill should be used when the user asks to "persist", "recap", "记录一下这个session", "总结一下", or invokes /persist. Reviews the current session and persists key learnings, decisions, and experiences to ~/.agent/. For quick single-item writes during a session, use /record instead.
---

# Persist

Review the current session and persist key learnings to `~/.agent/`.

Unlike `/record` (quick single-item write), `/persist` is for session-level recap —
look back at what happened, extract what's worth keeping.

## Workflow

1. Review the current session for:
   - Problems solved and their solutions
   - Decisions made and their rationale
   - New discoveries or insights
   - Anything the user explicitly asked to remember
2. Scan `~/.agent/` for semantic overlap. If found, ask: "和 `xxx.md` 有重叠，合并还是新建？"
3. Choose a filename that reflects both **content summary** and **scope**, using the appropriate prefix:
   - **`record-`** for completed facts, fixes, observations, and lessons learned.
   - **`todo-`** for planned but not yet done tasks, improvements, or ideas.
   - **`lore-`** for elevated general principles, methodologies, and distilled wisdom.
   - **`persist-`** for session-level architecture or design records.
   Good: `record-env-setup-uv-path.md`, `todo-statusline-weather-enhancement.md`, `lore-knowledge-base-file-naming-philosophy.md`
   Bad: `todos.md`, `design.md` (missing prefix, scope unclear)
   **Propose the filename to the user before writing.** Wait for confirmation or adjustment.
4. **One file, one topic.** Split session learnings into separate files by topic.
   Do not bundle unrelated knowledge into one recap file.
   Sorting and organizing into directories is handled by future skills (/sort, /weave, /bind, /tidy).
   For now, keep files flat in `~/.agent/`.
5. Write each file. Structure per file:
   - Context (1-2 lines: what was this about)
   - Key learnings (bulleted, actionable)
   - Decisions made (with rationale)
   - Open items (if any)
6. Git commit:
   ```bash
   cd ~/.agent && git add -A && git commit -m "<descriptive message>"
   ```
   If commit fails (not a git repo), run `git init` and retry.
   If the commit is purely a rename of the previous commit's file, use `--amend` instead of a new commit.

## Content Guidelines

- **One file, one topic.** Do not bundle unrelated knowledge into one recap file.
  Sorting and organizing into directories is handled by future skills (/sort, /weave, /bind, /tidy).
  For now, keep files flat in `~/.agent/`.
- Same language as user's input.
- Focus on **why**, not just **what** — rationale has more replay value than facts.
- Be concise — no fluff, no repetition.
- Include exact commands, file paths, or code where relevant.
- If appending to an existing file, read first, then edit.
