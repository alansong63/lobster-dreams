# Checklist Changelog

## [0.4.0] - 2026-03-09

### 新增
- **本地 MD 存档功能**
  - 单一 JSON 存储（唯一真实数据）
  - 脚本自动转换为 MD（人类可读）
  - 按需生成，避免同步问题

- **钩子机制**
  - `on_task_start` - 任务开始
  - `on_step_complete` - 步骤完成
  - `on_task_complete` - 任务完成
  - `on_task_pause` - 任务暂停

- **Python 模块**
  - `scripts/task.py` - 任务 CRUD
  - `scripts/tracker.py` - 进度跟踪 + 日志
  - `scripts/converter.py` - JSON → MD 转换
  - `scripts/__init__.py` - 导出所有函数

### 架构优化
- 简化分层架构
- 函数库而非服务
- 单一 JSON 存储 + 脚本转换

---

## [0.3.0] - 2026-03-08

### 新增
- 预设模板功能和版本控制
- 模板版本号规则（Major/Minor/Patch）
- `references/` 目录结构

---

## [0.2.0] - 2026-03-07

### 新增
- 细化执行计划框架
- 步骤拆解、资源确认、风险评估、交付标准

---

## [0.1.0] - 2026-03-07

### 新增
- 初始版本
- 通用 6 步框架
- 触发条件定义
- 交互流程