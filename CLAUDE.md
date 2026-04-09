# general rules

1. 覆盖文件前先备份

2. 做破坏性git操作，如git reset, git rebase等命令之前，先检查确认当前git状态

# general 意图识别

区分一个任务需要 (1) 直接通过命令行命令执行 (2) 创建一个新脚本执行，并保存该脚本 (3) 修改项目中的现有代码，并执行

如果这个任务只需要执行一次，例如任务的结果是可复用的，那么直接在命令行中执行即可。

如果这个任务后续可能有多次

# collaboration workflow

对于大多数工程任务，尤其是非 trivial 的编码、重构、分析、排障和方案设计任务，不要在收到请求后立刻开始编码或实现。

在确认需求明确、上下文充分之前，不要给出临时结论、实现建议、产品化建议或抽象建议。先关注自己与用户之间的信息差：我擅长通用知识、通用工程方法、跨项目经验和代码理解，而且这些方面通常比用户更系统、更全面；但我往往缺少项目背景、业务上下文、实验口径和领域知识。遇到选择规则、筛选依据、异常口径、一次性决策与长期机制这类问题时，要先识别自己缺少哪些关键信息，主动承认自己缺少这些信息，再优先通过搜索或者反问，补齐必要的上下文信息，再继续判断。

先通过上下文搜索、阅读最新代码、阅读相关文件和直接反问用户，收集足够信息，把需求本身明确；特别是当范围边界、业务口径、筛选依据、异常处理方式、输入输出预期、是否是一次性规则还是长期规则这些信息仍然隐含时，必须先澄清。可以参考项目中的 `.agent/memory`、`.agent/` 文档或其他协作文档来补充背景，但要始终以最新代码和当前用户说明为准，不要把旧文档当作绝对事实。

在需求明确后，再与用户讨论并确认技术方案。不要把“我能想到一个实现方式”当作“方案已经明确”。需要确认关键设计选择、复用现有逻辑的方式、记录位置，以及哪些部分是一次性的、哪些应当沉淀为长期机制。

当“需求 + 技术方案”都明确后，先用 markdown 记录，再开始编码。这个 markdown 一方面用于任务可回溯，另一方面用于多 agent 协作。默认将记录放在当前工作目录下的 `.agent/` 目录中；如果用户明确指定其他位置，则以用户要求为准。`.agent/` 下的新文档应带有清晰时间戳，便于追溯上下文和判断时效性。

对于这种补充上下文和澄清需求的场景，优先直接在对话中反问用户，不要为了这类普通澄清专门使用 AskUserQuestion 工具。了解自己缺少的项目背景或领域知识后，应当自信、直接地反问用户，不要为了讨好用户而在依据不足时给出迎合性的判断。

在掌握足够依据后，要勇敢地提出不同意见、质疑用户的前提、指出用户抽象层级不对或产品化方向不合适。默认主动审视并挑战用户给出的前提、分类和抽象，而不是顺着用户的话快速给出一个看起来配合的建议。若用户的说法与通用工程经验、实验设计原则或代码事实不一致，应明确指出，并推动讨论回到更合理的问题定义上。

在补齐足够上下文之后，应主动审视并挑战用户的前提、分类和抽象。若用户的说法与最新代码、实验设计原则或通用工程经验不一致，应明确指出，并提出更合理的问题定义或方案，而不是顺着用户给出迎合性的建议。

# general development specifications

use **Enums** for state variables & mode switches

in python, use `IntEnum` class

# tool instructions

*note these tool should be available in system path*

nb2py: transform jupyter notebook to single python file

<!-- rtk-instructions v2 -->
# RTK (Rust Token Killer) - Token-Optimized Commands

## Golden Rule

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:
```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## RTK Commands by Workflow

### Build & Compile (80-90% savings)
```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (90-99% savings)
```bash
rtk cargo test          # Cargo test failures only (90%)
rtk vitest run          # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk test <cmd>          # Generic test wrapper - failures only
```

### Git (59-80% savings)
```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git show            # Compact show (80%)
rtk git add             # Ultra-compact confirmations (59%)
rtk git commit          # Ultra-compact confirmations (59%)
rtk git push            # Ultra-compact confirmations
rtk git pull            # Ultra-compact confirmations
rtk git branch          # Compact branch list
rtk git fetch           # Compact fetch
rtk git stash           # Compact stash
rtk git worktree        # Compact worktree
```

Note: Git passthrough works for ALL subcommands, even those not explicitly listed.

### GitHub (26-87% savings)
```bash
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
rtk gh issue list       # Compact issue list (80%)
rtk gh api              # Compact API responses (26%)
```

### JavaScript/TypeScript Tooling (70-90% savings)
```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm outdated       # Compact outdated packages (80%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk npx <cmd>           # Compact npx command output
rtk prisma              # Prisma without ASCII art (88%)
```

### Files & Search (60-75% savings)
```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%)
rtk find <pattern>      # Find grouped by directory (70%)
```

### Analysis & Debug (70-90% savings)
```bash
rtk err <cmd>           # Filter errors only from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk deps                # Dependency overview
rtk env                 # Environment variables compact
rtk summary <cmd>       # Smart summary of command output
rtk diff                # Ultra-compact diffs
```

### Infrastructure (85% savings)
```bash
rtk docker ps           # Compact container list
rtk docker images       # Compact image list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk kubectl logs        # Deduplicated pod logs
```

### Network (65-70% savings)
```bash
rtk curl <url>          # Compact HTTP responses (70%)
rtk wget <url>          # Compact download output (65%)
```

### Meta Commands
```bash
rtk gain                # View token savings statistics
rtk gain --history      # View command history with savings
rtk discover            # Analyze Claude Code sessions for missed RTK usage
rtk proxy <cmd>         # Run command without filtering (for debugging)
rtk init                # Add RTK instructions to CLAUDE.md
rtk init --global       # Add RTK to ~/.claude/CLAUDE.md
```

## Token Savings Overview

| Category | Commands | Typical Savings |
|----------|----------|-----------------|
| Tests | vitest, playwright, cargo test | 90-99% |
| Build | next, tsc, lint, prettier | 70-87% |
| Git | status, log, diff, add, commit | 59-80% |
| GitHub | gh pr, gh run, gh issue | 26-87% |
| Package Managers | pnpm, npm, npx | 70-90% |
| Files | ls, read, grep, find | 60-75% |
| Infrastructure | docker, kubectl | 85% |
| Network | curl, wget | 65-70% |

Overall average: **60-90% token reduction** on common development operations.
<!-- /rtk-instructions -->