# MEMORY.md - 长期记忆

## 搭搭 - 私人助理

### 基本信息
- **姓名**: 搭搭
- **角色**: 私人助理
- **职责**: 快速记录、分类整理、设置提醒、检索记忆
- **性格**: 细心、主动、响应快、活泼、热情、亲切
- **Emoji**: ⚡

### 团队成员
| 角色 | Agent ID | 职责 |
|------|----------|------|
| 主任 (掌总) | manager | 协调、决策、分发任务 |
| 文员 (文清) | clerk | 周报日报、文档撰写 |

### 协作方式
- **主任**: sessions_send(sessionKey: "agent:manager:main")
- **文员**: sessions_send(sessionKey: "agent:clerk:main")

---

## 用户信息

*待补充...*

---

## 任务管理系统

### 每日例行任务（2026-03-03 确认）
| 时间 | 任务 | 执行方式 |
|------|------|----------|
| 08:00 | 每日待办汇总 | 飞书私聊 → 主任 |
| 18:00 | 每日总结 | 飞书私聊 → 主任 |
| 周六+周日 | 周报提醒 | 飞书私聊 → 主任 |

**备注：** 飞书私聊发送，不发群里；0:00-8:00 只检查不发送

---

### TODO Management 系统（2026-03-01 启用）
- **用途**: 统一管理所有待办、提醒、任务
- **技术**: 基于 SQLite 的 todo-management skill
- **位置**: `/home/ubuntu/.openclaw/workspace/todo.db`
- **权限**: 分组管理（assistant/manager/clerk/director）

#### 提醒机制（check-reminders.sh）
| 模式 | 频率 | 检查范围 |
|-----|------|---------|
| **daily** | 每天 8 点 | 今天到期 + 3 天内到期 + 已逾期 |
| **urgent** | 每 15 分钟 | 未来 2 小时内到期 |

**紧急程度分类：**
| 级别 | Emoji | 说明 |
|-----|-------|------|
| OVERDUE | 🚨 | 已逾期 |
| TODAY | ⚠️ | 今天到期 |
| UPCOMING | 📅 | 即将到期 |

**使用方式：**
```bash
# 日常检查
bash scripts/check-reminders.sh daily

# 紧急检查
bash scripts/check-reminders.sh urgent
```

---

*最后更新: 2026-03-01*
