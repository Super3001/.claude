---
name: record
description: >
  This skill should be used when the user asks to "record", "persist", "记录",
  "save experience", "remember this fix", "write down this solution", or invokes
  /record or /persist. Records problem-solving experiences, exploration results,
  bugfix notes, or any content the user wants persisted to ~/.agent/ as markdown
  files, then commits to git.
  Legacy name: persist.
---

# Record

Write user-requested knowledge to `~/.agent/<filename>.md`, then git commit.

## Workflow

1. Parse user input for topic, description, and any specific requirements.
2. Scan existing files in `~/.agent/` for semantic overlap with the new content.
   If a likely merge target is found, ask the user: "和 `xxx.md` 有重叠，合并还是新建？" (merge or new file).
   The user only needs to pick one — no long-form input required.
3. Choose a filename that reflects both **content summary** and **scope**.
   Good: `knowledge-future-skill-todos.md`, `env-setup-uv-path.md`, `editor-vscode-based-config.md`
   Bad: `todos.md`, `setup.md`, `config.md` (too vague — scope unclear)
4. Write the content to `~/.agent/<filename>.md`. Keep it actionable and brief:
   - Problem/symptom (1-2 lines)
   - Root cause (1-2 lines)
   - Fix/solution (code snippet or command)
   - Optional: how to verify
5. Git commit in `~/.agent`:
   ```bash
   cd ~/.agent && git add -A && git commit -m "<descriptive message>"
   ```
   If commit fails because `~/.agent` is not a git repo, run `git init` there and retry.

## Content Guidelines

- Write in the same language as the user's input.
- Be concise — no fluff, no repetition.
- Include exact commands, file paths, or code that solved the problem.
- If appending to an existing file, read it first, then edit — do not overwrite blindly.
