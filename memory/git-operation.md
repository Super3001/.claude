# Git 操作教训

## 2026-02-25: reset 前未确认当前 HEAD 状态

### 错误经过

1. 用户要求只提交 arkts-test-generator 下的文件，但我之前的 commit 包含了过多文件
2. 我直接执行了 `git reset --soft HEAD~1`，没有先用 `git log --oneline` 确认当前 HEAD 指向哪个 commit
3. 实际上用户可能已经自行做过 reset 或其他操作，我的 reset 因此多撤销了不该撤销的 commit（包括用户自己的 commit `8eb10b4`）
4. 最终用户不得不手动 cherry-pick 找回丢失的 commit

### 根本原因

在执行 `git reset` 之前，没有确认"即将 reset 的 commit 是否是我需要撤销的，还是用户已经处理过了"。盲目假设当前 HEAD 状态与自己上次操作后一致。

### 正确做法

**执行任何 git reset / rebase 之前，必须：**

1. 先 `git log --oneline -5` 确认当前 HEAD 和最近的 commit 链
2. 确认即将被撤销的 commit 确实是需要撤销的（对比 commit id）
3. 如果用户中间可能做过操作（比如对话中有中断、用户手动执行了命令），更要先确认当前状态
4. 对于破坏性操作（reset、rebase 等），如果前一个操作不是确定是自己进行（例如用户发出指令，那么用户有可能在中间进行了操作），那么状态可能会有变化，此时操作之前必须确认一次状态，不要假设状态
