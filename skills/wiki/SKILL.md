---
name: wiki
description: >
  This skill should be used when the user asks to "摄入", "ingest", "lint wiki",
  "query wiki", "查一下wiki", "wiki", or invokes /wiki. Operates the LLM Wiki at
  D:\Obsidian\LLM-Wiki from any directory. Supports three operations: ingest (摄入),
  query (查询), and lint (健康检查).
---

# Wiki

Operate the LLM Wiki at `D:\Obsidian\LLM-Wiki` from any working directory.

## Setup

Before any operation, read the schema:
```bash
cat "D:\Obsidian\LLM-Wiki\CLAUDE.md"
```
This loads the project structure, page conventions, and operation rules.

## Operations

### Ingest (摄入)

Trigger: user says "摄入 [source]" or "ingest [source]"

1. Read the source file from `D:\Obsidian\LLM-Wiki\raw/`
2. Discuss key points with user
3. Create or update pages in `D:\Obsidian\LLM-Wiki\wiki/`
4. Update `wiki/index.md`
5. Append entry to `wiki/log.md`
6. Commit:
   ```bash
   cd "D:\Obsidian\LLM-Wiki" && git add -A && git commit -m "ingest: [source title]"
   ```

### Query (查询)

Trigger: user asks a knowledge question mentioning "wiki"

1. Read `D:\Obsidian\LLM-Wiki\wiki\index.md` to locate relevant pages
2. Read those pages
3. Synthesize answer with `[[wiki-links]]`
4. If answer is valuable, propose archiving as new page

### Lint (健康检查)

Trigger: user says "lint wiki" or "wiki lint"

1. Check for contradictions between pages
2. Find orphan pages (no inbound links)
3. List frequently mentioned concepts without their own page
4. Flag outdated conclusions superseded by newer sources
5. Suggest next investigation questions

## Page Convention

Every wiki page must include YAML frontmatter:

```yaml
---
title: Page Title
type: concept | entity | comparison | note
sources: [list of raw/ files referenced]
related: [list of wiki pages linked]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```
