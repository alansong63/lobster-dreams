---
name: task-checklist
description: 长程任务 checklist 管理框架。帮助 AI agent 在执行长程任务时保持进度追踪，确保任务不会因上下文中断而丢失进度。支持动态创建、更新、完成 checklist。支持本地 MD 存档和自动进度跟踪。
version: 0.4.0
---

# Task Checklist

长程任务的进度追踪工具，确保任务不会"断片"。

## 触发条件

**会触发：**
- "帮我做 xxx"
- "开始做 xxx"
- "创建个 checklist"
- "建个任务清单"
- "记录 xxx 决策"
- "记录 xxx 问题"
- 任何需要多步骤完成的任务

**不会触发：**
- 简单问答
- 查询类任务

---

## 通用框架（必用）

所有任务使用这个通用框架：

```
[ ] 1. 需求定义 - 要做什么？
[ ] 2. 研发目标 - 做到什么程度？
[ ] 3. 执行计划 - 怎么做？
[ ] 4. 实施执行 - 具体实现
[ ] 5. 自检验证 - 做完了吗？
[ ] 6. 完成交付 - 结束
```

---

### 第3步执行计划详解

执行计划是 checklist 最关键的一步，必须做细：

```
[ ] 3. 执行计划 - 怎么做？
    ├── 步骤拆解 - 分成哪几步？
    ├── 资源确认 - 需要什么？（工具/权限/信息）
    ├── 风险评估 - 有什么问题？
    └── 交付标准 - 怎么算完成？
```

#### 3.1 步骤拆解

把大任务拆成小步骤，每步可执行：

```
示例：
- 创建 GitHub 仓库
- 推送代码
- 添加主题标签
```

#### 3.2 资源确认

执行前确认需要的资源：

```
示例：
- gh CLI 已安装
- GitHub 账号有权限
- 必要的环境变量
```

#### 3.3 风险评估

预估可能的问题：

```
示例：
- 分支名可能不一致
- 仓库可能已存在
- 网络可能不稳定
```

#### 3.4 交付标准

明确怎么算完成：

```
示例：
- 4 个仓库都能访问
- 每个有正确文件
- 本地文件未被移动
```

---

## 触发后交互流程

### 创建时

1. 展示 checklist 框架
2. 询问需求
3. 填充每一步详情
4. **自动创建 JSON + MD 存档**

### 执行中

1. 每完成一步更新状态
2. 显示进度百分比
3. 提示下一步
4. **自动记录日志和更新 MD**

### 中断恢复

1. 检测未完成任务
2. 读取 MD 存档恢复上下文
3. 询问是否继续
4. 恢复到断点

---

## 使用示例

### 示例 1：开始新任务
```
用户：帮我做个 workspace-cleanup skill

我：好的，为你创建 checklist：

📋 Task Checklist
━━━━━━━━━━━━━━━━━━━━

[ ] 1. 需求定义 - 要做什么？
[ ] 2. 研发目标 - 做到什么程度？
[ ] 3. 执行计划 - 怎么做？
[ ] 4. 实施执行 - 具体实现
[ ] 5. 自检验证 - 做完了吗？
[ ] 6. 完成交付 - 结束

━━━━━━━━━━━━━━━━━━━━

✅ 任务已创建：task-20260309-xxxx
✅ MD 存档已生成

**第1步：需求定义**
请告诉我：这个任务要做什么？
```

### 示例 2：更新进度
```
用户：需求是整合 4 个 skills 到 GitHub

我：✓ 更新进度：

📋 Task Checklist
━━━━━━━━━━━━━━━━━━━━
[✓] 1. 需求定义 - 整合 4 个 skills 到 GitHub
[ ] 2. 研发目标 - 4 个独立仓库 + 主题归类
[ ] 3. 执行计划 - 怎么做？
[ ] 4. 实施执行 - 具体实现
[ ] 5. 自检验证 - 做完了吗？
[ ] 6. 完成交付 - 结束

进度：1/6 (17%)

✅ 日志已记录
✅ MD 存档已更新

**第2步：研发目标**
这个任务要做到什么程度才算完成？
```

### 示例 3：记录决策
```
用户：我觉得用 JSON + MD 双存储比较好

我：✓ 记录决策：

✅ 决策已记录：
| 时间 | 决策 | 理由 |
|------|------|------|
| 16:00 | 使用 JSON + MD 双存储 | 避免双存储同步问题 |

✅ MD 存档已更新
```

### 示例 4：恢复任务
```
用户：继续之前那个任务

我：📋 恢复任务：task-20260309-xxxx

当前状态：🔄 进行中 (33%)
上次更新：2026-03-09 16:00

📌 需求：整合 4 个 skills 到 GitHub

📝 最新日志：
16:00 - 完成第1步：需求定义

🔜 下一步：
- [ ] 2. 研发目标

是否继续？ [Y/n]
```

---

## 本地存档功能 (v0.4.0 新增)

### 存储结构

```
~/.openclaw/workspace/.checklist/
└── tasks/
    ├── task-20260309-001.json  ← 任务数据（唯一真实数据）
    └── task-20260309-001.md     ← 存档（按需生成）
```

### JSON 数据格式

```json
{
  "id": "task-20260309-001",
  "title": "任务标题",
  "status": "in_progress",
  "created": "2026-03-09T16:00:00Z",
  "updated": "2026-03-09T16:30:00Z",
  "progress": {
    "total": 6,
    "completed": 2,
    "percentage": 33
  },
  "steps": [
    {"id": 1, "content": "需求定义", "status": "completed"},
    {"id": 2, "content": "研发目标", "status": "in_progress"}
  ],
  "logs": [
    {"time": "2026-03-09T16:00:00Z", "action": "创建任务", "detail": "..."}
  ],
  "decisions": [
    {"time": "2026-03-09T16:10:00Z", "decision": "...", "reason": "..."}
  ],
  "problems": [
    {"time": "2026-03-09T16:15:00Z", "problem": "...", "solution": "..."}
  ]
}
```

### MD 存档格式

```markdown
# 任务：xxx

## 📌 基本信息
- **ID**: task-xxx
- **状态**: 🔄 进行中
- **进度**: 33% (2/6)

## 📋 执行计划
- [x] 1. 需求定义 ✅
- [ ] 2. 研发目标 🔄
- [ ] 3. 执行计划

## 💡 关键决策
| 时间 | 决策 | 理由 |
|------|------|------|
| 16:10 | xxx | xxx |

## 🔧 问题与解决
### ❓ 问题描述
- **解决**: 解决方案

## 📝 执行日志
### 16:00
- 创建任务

## 📌 下一步
- [ ] 2. 研发目标
```

---

## 钩子机制 (v0.4.0 新增)

自动追踪状态变化：

| 钩子 | 触发时机 | 作用 |
|------|----------|------|
| `on_task_start` | 任务开始 | 记录开始时间 |
| `on_step_complete` | 步骤完成 | 更新进度、记录日志 |
| `on_task_complete` | 任务完成 | 记录完成时间 |
| `on_task_pause` | 任务暂停 | 记录暂停原因 |

---

## Python 模块

### scripts/task.py - 任务 CRUD

```python
from scripts import create_task, get_task, list_tasks

task_id = create_task("任务标题")
task = get_task(task_id)
tasks = list_tasks()
```

### scripts/tracker.py - 进度跟踪

```python
from scripts import start_task, complete_task, log_action
from scripts import add_decision, add_problem

start_task(task_id)
complete_task(task_id)
log_action(task_id, "完成步骤1")
add_decision(task_id, "决策内容", "理由")
add_problem(task_id, "问题描述", "解决方案")
```

### scripts/converter.py - 格式转换

```python
from scripts import json_to_md, sync_md, read_md

md_path = json_to_md(task_id)  # JSON → MD
sync_md(task_id)                # 强制同步
content = read_md(task_id)     # 读取 MD
```

---

## 预设模板 (references/)

### 模板存放位置
- 路径：`references/`
- 格式：Markdown 文件
- 命名：`<task-type>-template.md`

### 模板版本控制

每个模板文件必须包含版本信息：

```markdown
> **版本**: 1.0.0
> **适用**: xxx
> **更新日期**: 2026-03-08
```

### 版本号规则

| 位数 | 含义 | 示例 |
|------|------|------|
| Major | 重大结构变更 | 1.0.0 → 2.0.0 |
| Minor | 新增模板 | 1.0.0 → 1.1.0 |
| Patch | 修复/优化 | 1.0.0 → 1.0.1 |

### 已有模板

| 模板文件 | 版本 | 适用场景 |
|----------|------|----------|
| plugin-install-template.md | 1.0.0 | OpenClaw 插件安装 |

---

## 数据存储

文件位置：`~/.openclaw/workspace/.checklist/`

格式：
```json
{
  "task_id": "xxx",
  "title": "任务标题",
  "created": "2026-03-07T22:00:00Z",
  "status": "in_progress",
  "steps": [
    {
      "id": 1,
      "content": "需求定义",
      "detail": "整合 4 个 skills 到 GitHub",
      "status": "completed"
    },
    {
      "id": 2,
      "content": "研发目标",
      "detail": "4 个独立仓库 + 主题归类",
      "status": "pending"
    }
  ]
}
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.4.0 | 2026-03-09 | 新增本地 MD 存档、钩子机制、Python 模块 |
| 0.3.0 | 2026-03-08 | 新增预设模板功能和版本控制 |
| 0.2.0 | 2026-03-07 | 细化执行计划框架 |
| 0.1.0 | 2026-03-07 | 初始版本 |

---

## 交付物标准

每个 skill 交付时必须包含：

| 文件 | 说明 |
|------|------|
| SKILL.md | 技能说明 |
| README.md | 使用文档 |
| CHANGELOG.md | 变更历史 |
| _meta.json | 版本元数据 |

---

**版本**: 0.4.0