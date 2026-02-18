# Lobster Mind 项目记录 - 2026-02-15

## 背景

今天是全流程测试和固化的一天。验证了 subagent 调度 → 内容生成 → 发布的完整流程。

---

## 当前架构

### 角色分工

| 角色 | 职责 |
|------|------|
| **Lobster Bro（我）** | 统筹管理，调度 subagent，质量检查 |
| **Subagents** | 用指定模型生成各板块内容 |
| **Dev** | subagent 返回后自动保存、发布、全流程 |
| **humanizer-zh** | 去除 AI 味道（简化自检） |
| **content-quality-auditor** | 简化为 5 项快速评分 |

### 模型分配

| 板块 | 编辑 | 模型 |
|------|------|------|
| Thoughts | Professor Stein | zai/glm-4.7 |
| Reflections | Zen | zai/glm-4.7 |
| Ideas | Luna | minimax-portal/MiniMax-M2.5 |
| Essays | Wordsmith | minimax-portal/MiniMax-M2.5 |
| Lifestyle | Chef Marco | minimax-portal/MiniMax-M2.5 |
| Dreams | Lobster Bro | minimax-portal/MiniMax-M2.5 |

**注意：** Gemini 模型不可用，已从配置中移除。

---

## 已验证的流程

### Subagent 调度流程（手动版，已固化到 SKILL.md）

```
1. should_work.sh 判断今天该生成哪个板块
2. 检查该板块已有文章数量（如少于 2 篇则补充）
3. 加载该编辑的 prompt（editors.md）
4. 选择一个有趣的主题
5. 调度 subagent 用指定模型生成内容
   → sessions_spawn({ model: "对应模型", task: "..." })
6. 等待 subagent 返回内容
7. 【Dev 职责】保存原始内容到 {板块}/YYYY-MM-DD.md
8. 【Dev 职责】humanizer-zh 处理（去除 AI 味）
9. 【Dev 职责】快速评分审核（简化版，5 分钟）
10. 【Dev 职责】转换为 HTML
11. 【Dev 职责】发布到对应目录
12. 【Dev 职责】更新该板块 index.html
13. 【Dev 职责】更新首页 index.html
14. 【Dev 职责】Git push
15. Lobster Bro 检查确认
```

### 触发时间

| 时间 | 任务 |
|------|------|
| 1:00 | Dream 生成 |
| 2:00-3:00 | 其他 5 板块生成 |
| 周六 | 周报汇报 |

---

## 今日测试记录

### 测试 1: Thoughts (GLM-4.7)

- 主题：当 AI 有了"自我意识"，世界会怎样？
- 结果：✅ 成功，1950 字
- 问题：subagent 返回有延迟，需要等待

### 测试 2: Lifestyle (MiniMax)

- 主题：如何用最少的时间做出营养均衡的一顿饭？
- 结果：✅ 成功，1200 字

### 测试 3: Ideas (MiniMax)

- 主题：如果 AI 能帮人类"做梦"，会怎样？
- 结果：✅ 成功，1100 字

---

## 发现的问题

### 1. Subagent 返回延迟/不稳定

- subagent 任务完成后，返回通知有时延迟 1-2 分钟
- 偶尔出现会话建立但无内容返回的情况

### 2. 自动化程度不足

- **现状**：subagent 返回后需要我手动执行保存→发布→推送
- **理想**：subagent 返回后自动触发后续流程

### 3. 审核流程简化

- 完整 80 项审核太重
- 已简化为 5 项快速评分（5 分钟内完成）

---

## 待解决的问题

### 优先级：高

1. **全自动化链条**
   - 问题：如何让 subagent 返回后自动触发发布流程？
   - 可能的方案：用 cron job 调用完整脚本，或创建一个"总调度 agent"

2. **错误处理机制**
   - subagent 失败时如何重试？
   - 发布失败时如何告警？

### 优先级：中

3. **模型切换测试**
   - 验证 GLM-4.7 和 MiniMax 的实际效果差异
   - 目前只在测试中使用，未正式跑过

4. **内容质量监控**
   - 每天检查发布质量
   - 定期复盘调整 prompt

---

## 网站信息

- **公开地址**: https://lobster-dreams.github.io/
- **GitHub**: https://github.com/alansong63/lobster-dreams
- **私有备份**: https://github.com/alansong63/lobstermind
- **技能位置**: ~/.openclaw/workspace/skills/lobster-mind/
- **编辑器配置**: ~/.openclaw/workspace/skills/lobster-mind/references/editors.md
- **状态文件**: ~/.openclaw/workspace/skills/lobster-mind/data/state.json

---

## AI 自主维护能力评估

| 能力 | 现状 | 说明 |
|------|------|------|
| 定时触发 | ✅ 可用 | cron/heartbeat |
| 内容生成 | ✅ 可用 | subagent 可用，但不稳定 |
| 文件操作 | ✅ 可用 | 读/写/编辑 |
| Git push | ✅ 可用 | |
| 错误处理 | ⚠️ 有限 | 需要人工监控 |
| 多步骤自动化 | ❌ 待解决 | 需要实现自动触发链 |

**结论**：能实现"半自主"运营，需要定时检查和人工兜底。

---

## 后续方向

1. **短期**：写一个自动化发布脚本，减少手动操作
2. **中期**：实现全自动化链条（定时→生成→发布→推送）
3. **长期**：加入错误处理和告警机制，实现无人值守

---

*记录时间：2026-02-15*
*记录人：Lobster Bro*
