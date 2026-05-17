# Sort History HTML Specification

After each sort operation, write/update `~/.agent/sort-history.html`.
The file is a standalone, self-contained HTML page that logs all sort operations.

## File Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sort History — ~/.agent/</title>
<style>
  /* Inline CSS — no external dependencies */
  :root {
    --bg: #f8f9fa;
    --card-bg: #ffffff;
    --text: #212529;
    --text-muted: #6c757d;
    --border: #dee2e6;
    --accent: #0d6efd;
    --accent-light: #e7f1ff;
    --mono: "Cascadia Code", "Fira Code", "JetBrains Mono", "Consolas", monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 2rem;
    max-width: 960px;
    margin: 0 auto;
  }
  h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
  .subtitle { color: var(--text-muted); margin-bottom: 2rem; font-size: 0.9rem; }

  /* Sort entry card */
  .sort-entry {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .sort-entry h2 {
    font-size: 1.1rem;
    display: flex; align-items: center; gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
  }
  .sort-entry .id-badge {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--text-muted);
    background: var(--bg);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }
  .sort-entry h3 {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
  }

  /* Stats row */
  .stats-row {
    display: flex; gap: 1rem; flex-wrap: wrap;
    margin-bottom: 1rem;
  }
  .stat {
    background: var(--accent-light);
    color: var(--accent);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
  }

  /* Moves table */
  .moves-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin-bottom: 1rem;
  }
  .moves-table th {
    text-align: left;
    padding: 0.4rem 0.5rem;
    background: var(--bg);
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--text-muted);
    border-bottom: 2px solid var(--border);
  }
  .moves-table td {
    padding: 0.35rem 0.5rem;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  .moves-table .from { font-family: var(--mono); font-size: 0.82rem; }
  .moves-table .to   { font-family: var(--mono); font-size: 0.82rem; color: #198754; }
  .moves-table .dir  { font-weight: 600; color: var(--text-muted); font-size: 0.8rem; }

  /* Tree */
  .tree-view {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-family: var(--mono);
    font-size: 0.82rem;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre;
    color: var(--text);
  }

  /* Scheme description */
  .scheme-note {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }

  /* Empty state */
  .empty-state {
    text-align: center;
    color: var(--text-muted);
    padding: 3rem;
    font-style: italic;
  }

  /* Summary header */
  .summary-bar {
    display: flex; gap: 0.75rem; align-items: center;
    margin-bottom: 2rem;
    padding: 0.75rem 1rem;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
  }
  .summary-bar .total { font-weight: 700; font-size: 1.5rem; color: var(--accent); }
  .summary-bar .label { font-size: 0.85rem; color: var(--text-muted); }
</style>
</head>
<body>

<h1>&#128451; Sort History</h1>
<p class="subtitle"><code>~/.agent/</code> directory sort operations</p>

<div class="summary-bar">
  <div><span class="total">N</span> <span class="label">total sorts</span></div>
  <div><span class="total">M</span> <span class="label">files moved</span></div>
  <div><span class="total">D</span> <span class="label">directories</span></div>
</div>

<!-- SORT ENTRY TEMPLATE — append new entries at top -->
<div class="sort-entry" id="sort-YYYYMMDD-HHMMSS">
  <h2>
    YYYY-MM-DD HH:MM
    <span class="id-badge">#N</span>
  </h2>

  <div class="stats-row">
    <span class="stat">M files moved</span>
    <span class="stat">D dirs created</span>
  </div>

  <div class="scheme-note">
    <strong>Scheme:</strong> <description of classification logic>
  </div>

  <h3>Files Moved</h3>
  <table class="moves-table">
    <thead>
      <tr><th>From</th><th>To</th></tr>
    </thead>
    <tbody>
      <tr><td class="from">root/file.md</td><td class="to">dir/file.md</td></tr>
    </tbody>
  </table>

  <h3>Directory After Sort</h3>
  <pre class="tree-view">dir/
├── file.md
└── subdir/
    └── file.md</pre>
</div>
<!-- END SORT ENTRY -->

</body>
</html>
```

## Generation Rules

### First Sort (File Doesn't Exist)

Create the file from scratch with the full HTML skeleton above, populated with the first sort entry.

### Subsequent Sorts (File Exists)

1. Read existing `~/.agent/sort-history.html`
2. Insert new `<div class="sort-entry">` after the summary-bar, before the first existing sort-entry (newest first)
3. Update summary-bar totals (total sorts, total files moved, total directories)
4. Do NOT rewrite the entire file — parse and insert precisely

### Sort Entry ID Format

`sort-YYYYMMDD-HHMMSS` — local time of the sort operation.

### Tree Format

Use `tree`-style output:
```
ai-infra/
├── file-a.md
├── file-b.md
env/
├── file-c.md
├── file-d.md
```

### Scheme Description

One sentence describing the classification logic. Examples:
- "Grouped by topic: experience files → experience/, records → ai-tools/"
- "Merged ai-infra/ split into ai-infra/ and ai-tools/ by provider vs tooling"

## Edge Cases

- **Empty sort (nothing to move):** Still write an entry. Scheme: "No files to sort — root already clean."
- **Sort that only renames (no moves):** Record as moves but note "rename only" in scheme.
- **Pre-existing directories not touched:** Do NOT list them in "Files Moved" table. Only list files actually moved by this sort operation.
