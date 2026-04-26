---
name: record
description: This skill should be used when the user asks to "record", "write down", "记一下", "写下来", or invokes /record. Quickly write a single piece of knowledge to ~/.agent/ at any point during a session. For session-level recap, use /persist instead.
---

# Record

Quickly write a single piece of knowledge to `~/.agent/<filename>.md`.

Unlike `/persist` (session recap), `/record` is for immediate, atomic writes —
one fact, one fix, one observation, right now.

## Workflow

1. Parse user input for the specific item to record.
2. Scan `~/.agent/` for semantic overlap. If found, ask: "和 `xxx.md` 有重叠，合并还是新建？"
3. Choose a filename that reflects both **content summary** and **scope**, using the appropriate prefix:
   - **`record-`** for completed facts, fixes, observations, and lessons learned.
   - **`todo-`** for planned but not yet done tasks, improvements, or ideas.
   Good: `record-env-setup-uv-path.md`, `todo-statusline-weather-enhancement.md`
   Bad: `setup.md`, `config.md`, `env-setup-uv-path.md` (missing prefix)
   **Propose the filename to the user before writing.** Wait for confirmation or adjustment.
4. Write the content. Be brief and actionable.
5. Git commit:
   ```bash
   cd ~/.agent && git add -A && git commit -m "<descriptive message>"
   ```
   If commit fails (not a git repo), run `git init` and retry.
   If the commit is purely a rename of the previous commit's file, use `--amend` instead of a new commit.

## Content Guidelines

- **One file, one topic.** Do not bundle unrelated knowledge into one file.
  Sorting and organizing into directories is handled by future skills (/sort, /weave, /bind, /tidy).
  For now, keep files flat in `~/.agent/` — one fact per file is better than one file per session.
- Same language as user's input.
- Concise — no fluff, no repetition.
- Include exact commands, file paths, or code.
- If appending to an existing file, read first, then edit.
