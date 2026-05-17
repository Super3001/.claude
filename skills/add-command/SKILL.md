---
name: add-command
description: This skill should be used when the user asks to "add a new command", "create a script", "add a tool", "write a new utility", "add an alias command", "modify a command", "change a command", or wants to create/modify a CLI command in the usercmd project.
---

# Add / Modify Command

Add a new CLI command or modify an existing one in the usercmd project.

## Locate USERCMD_DIR

Resolution order:
1. `$MAIN_ROOT/Dev/usercmd` (where `MAIN_ROOT` is an environment variable)
2. Search for `**/usercmd` if step 1 fails

If found path differs from expected, ask user to confirm.

## Procedure & Conventions

### Adding a new command

Follow the **"Adding a new tool"** section in the project's `CLAUDE.md` for:
- Full procedure (naming → create → register → install)
- Coding conventions
- Completion checklist

### Modifying an existing command

1. Locate script in `scripts/` directory
2. Read current implementation
3. Apply requested changes following project conventions (see `CLAUDE.md`)
4. Run `install-usercmd -f` if entry point signature changed
