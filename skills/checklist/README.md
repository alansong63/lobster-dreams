# Task Checklist

🗒️ Long-running task checklist framework for AI agents.

![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Description

Task checklist helps AI agents track progress during long-running tasks, ensuring no step is forgotten due to context loss.

## Features

- ✅ Create checklist for any task
- ✅ Track progress step by step
- ✅ Dynamic adjustment (add/remove/reorder steps)
- ✅ Resume from interruption
- ✅ Standard workflow template
- 📋 **Preset templates** for common tasks
- 💾 **Local MD archive** - JSON as single source of truth, auto-generate MD for human readability
- 🔗 **Hook mechanism** - Auto-track state changes
- 🐍 **Python modules** - Easy integration with scripts

## Quick Start

```
User: 帮我做个 xxx

Bot: 创建 checklist：
[ ] 1. 需求定义
[ ] 2. 研发目标
[ ] 3. 执行计划
[ ] 4. 实施执行
[ ] 5. 自检验证
[ ] 6. 完成交付
```

## Standard Workflow

```
[ ] 1. 需求定义 - 要做什么？
[ ] 2. 研发目标 - 做到什么程度？
[ ] 3. 执行计划 - 怎么做？
    ├── 步骤拆解
    ├── 资源确认
    ├── 风险评估
    └── 交付标准
[ ] 4. 实施执行 - 具体实现
[ ] 5. 自检验证 - 做完了吗？
[ ] 6. 完成交付 - 结束
```

## Architecture

```
user message (feishu)
    ↓
SKILL.md (trigger + logic)
    ↓
scripts/ (Python functions)
    ↓
.checklist/tasks/ (JSON + MD)
```

### Python Modules

| Module | File | Purpose |
|--------|------|---------|
| task.py | scripts/task.py | Task CRUD |
| tracker.py | scripts/tracker.py | Progress tracking + hooks |
| converter.py | scripts/converter.py | JSON → MD conversion |

### Usage

```python
from scripts import create_task, start_task, add_decision
from scripts import json_to_md, read_md

# Create and manage tasks
task_id = create_task("My Task")
start_task(task_id)
add_decision(task_id, "Use JSON+MD", "Avoid sync issues")

# Generate MD archive
md_path = json_to_md(task_id)
content = read_md(task_id)
```

## Hooks

Auto-track state changes:

| Hook | Trigger |
|------|---------|
| on_task_start | Task starts |
| on_step_complete | Step completed |
| on_task_complete | Task completed |
| on_task_pause | Task paused |

## Storage

```
~/.openclaw/workspace/.checklist/
└── tasks/
    ├── task-xxx.json  # Task data (single source of truth)
    └── task-xxx.md    # Archive (auto-generated)
```

## Preset Templates

Located in `references/` folder:

| Template | Version | Use Case |
|----------|---------|----------|
| [plugin-install-template.md](references/plugin-install-template.md) | 1.0.0 | OpenClaw plugin installation |

### Using Templates

1. Check `references/` for existing templates
2. If no template exists, create one using the framework in SKILL.md
3. Follow version control rules when updating templates

### Version Control Rules

| Change | Version Bump |
|--------|--------------|
| Major structure changes | x.0.0 |
| New template added | 1.x.0 |
| Fix/optimization | 1.0.x |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.4.0 | 2026-03-09 | Add local MD archive, hook mechanism, Python modules |
| 0.3.0 | 2026-03-08 | Add preset templates and version control |
| 0.2.0 | 2026-03-07 | Detailed execution plan framework |
| 0.1.0 | 2026-03-07 | Initial release |

## More Info

See [SKILL.md](SKILL.md) for detailed documentation.

---

**Author**: AlanSong  
**License**: MIT  
**Version**: 0.4.0