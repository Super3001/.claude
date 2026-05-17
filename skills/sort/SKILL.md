---
name: sort
description: This skill should be used when the user asks to "sort", "整理", "归类", "分拣", "整理一下~/.agent", or invokes /sort. Also automatically triggered after /record or /persist when root-level .md files in ~/.agent/ exceed 20. Organizes flat files into topic-based subdirectories.
---

# Sort

Organize flat files in `~/.agent/` into topic-based subdirectories.

## When to Sort

- Root-level `.md` files in `~/.agent/` exceed 20
- User explicitly requests organization

## Design Principles

- **Surface-level topic classification.** Group by obvious subject, not by abstract taxonomy. Simple and intuitive, easy to execute correctly.
- **One axis only.** Pick one dimension (topic/scenario) and stick to it. Do not mix axes (e.g., some by file type, some by topic).
- **Cross-references are /weave's job.** Do not attempt to build links or cross-references during sort.
- **Ask before acting.** Classification is subjective. Always propose schemes, get user confirmation, then execute.

## Workflow

1. **Assess current state.** Count root-level `.md` files. List existing subdirectories and their contents.

2. **Ask the user one question at a time** to understand their preferred grouping logic before proposing any scheme. Example questions:
   - "What dimension should the directories be organized by? Topic, file nature, or application scenario?"
   - "Where does file X belong in your mental model?"
   Continue asking until 95% confident in the classification logic.

3. **Propose 2-3 schemes** with concrete file assignments. Each scheme is a table of `{directory → files}`. Present as side-by-side options.

4. **Wait for user to choose or adjust.** Incorporate feedback. Re-propose if needed.

5. **Execute moves.**
   - Create new directories as needed.
   - Move files to target directories.
   - Rename files only if user explicitly requests (e.g., adding a prefix).
   - Do not rename files on your own initiative.

6. **Verify.** Show final directory tree. Confirm all files accounted for.

7. **Write sort history.** After moves are committed, update `~/.agent/sort-history.html`:
   - If the file does not exist, create it from the full HTML skeleton.
   - If it exists, read it and insert a new sort-entry div after the summary bar (newest first).
   - Each entry records: timestamp, sort ID, scheme description, files moved (from → to), final directory tree.
   - Update the summary bar totals (total sorts, total files moved, total directories).
   - Full HTML format specification in **`references/sort-history-html.md`**.

## Existing Directory Structure

Current known directories in `~/.agent/` (may evolve):

| Directory | Topic |
|-----------|-------|
| `env/` | Development environment configuration (shell, editor, OS) |
| `ai-infra/` | AI infrastructure (providers, harness, OpenClaw) |
| `ai-tools/` | AI tool usage (skills, session records, design docs) |
| `experience/` | Development experience and lessons |
| `knowledge-engineering/` | Knowledge management (wiki, naming philosophy) |
| `report/` | Bug reports |

When new topics emerge with enough files (>= 3), propose creating a new directory.

## Prefix System

Files use semantic prefixes. Do not strip or change prefixes during sort unless user asks:

| Prefix | Meaning |
|--------|---------|
| `record-` | Completed facts, experiences, lessons |
| `todo-` | Planned but not done |
| `lore-` | Elevated principles and methodologies |
| `design-` | Specific design documents |
| `session-` | Session-level comprehensive records |
| `knowledge-` | Meta knowledge about the system |

## Pipeline Context

Sort is one step in the knowledge management pipeline:

```
/record    — write down (flat in root)
/sort      — organize into directories (this skill)
/weave     — cross-reference and link
/tidy      — deduplicate and clean up
```

Files written by `/record` and `/persist` land flat in root. Sort moves them into directories. This makes new files visible at a glance.
