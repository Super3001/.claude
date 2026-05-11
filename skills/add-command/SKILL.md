---
name: add-command
description: This skill should be used when the user asks to "add a new command", "create a script", "add a tool", "write a new utility", "add an alias command", or wants to create a new CLI command in the usercmd project.
---

# Add Command

Add a new CLI command to the usercmd project.

## Usercmd dir

USERCMD_DIR defaults to `C:/Dev/usercmd`. If that path does not exist, search for the correct usercmd directory (common alternatives: `M:/Dev/usercmd`). Ask user to confirm if a different dir is found.

## Procedure

### 1. Determine script name

Derive two names from the user's request:
- **File name**: `scripts/<snake_case>.py`
- **Command name**: kebab-case (registered in pyproject.toml)

Example: "add a which command" → file `scripts/which.py`, command `which`

### 2. Create the Python script

Write `scripts/<snake_case>.py` following this pattern:

```python
import sys


def main():
    # logic here
    pass


if __name__ == "__main__":
    main()
```

Use only standard library unless the functionality requires it. If a new dependency is needed, add it to `dependencies` in pyproject.toml.

Additional conventions (from CLAUDE.md):
- Use `IntEnum` for state variables and mode switches
- Include a `--check` flag for pre-run environment/data validation when applicable

### 3. Register entry point

Add one line to `[project.scripts]` in pyproject.toml:

```
<kebab-case> = "scripts.<snake_case>:main"
```

Keep the block alphabetically sorted.

### 4. Install globally

```bash
uv tool install --editable .
```

This makes the new command available system-wide. Existing scripts remain functional; only new entry points get registered.

## Checklist

Before reporting done, verify:
- `scripts/<name>.py` exists with a `main()` function
- pyproject.toml `[project.scripts]` has the new entry, alphabetically sorted
- `uv tool install --editable .` succeeds and lists the new executable
