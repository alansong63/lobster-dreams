# TODO

## 2026-02-16

### WebMCP 测试
- 待 Alan 升级飞书客户端后，获取截图内容
- 测试 Chrome 146 WebMCP 功能
- 编写 WebMCP 检测脚本

### 状态：待处理

---

## capability-evolver 定时任务配置

### 任务内容
- 每天 7:00 运行 `node index.js run --review`
- 每天 9:00 读取报告发送给 Alan 审核

### 待确认事项
- review 模式不会真正暂停等待确认，流程自动跑完
- 需要确认是否接受"自动跑完 + 9点发送报告"的流程

### 状态：待处理

---

## Lobster Mind 工作流优化

### 背景
SKILL.md 太长（299行），上下文容易丢失，需要结合 Checkpoint + Context Engineering 优化。

### 拆解（6阶段）

#### 阶段1：状态机基础设施
- 1.1 设计状态结构（state.json schema）
- 1.2 创建状态管理器（Python 脚本）
- 1.3 定义步骤枚举（15+步骤编号）

#### 阶段2：SKILL.md 模块化
- 2.1 拆分为独立文档（editors.md、workflow.md、steps/*.md）
- 2.2 主 SKILL.md 瘦身到 <100 行
- 2.3 创建入口脚本 run-workflow.py

#### 阶段3：Context Engineering
- 3.1 设计短 prompt 模板（每步 <2K tokens）
- 3.2 实现上下文加载器
- 3.3 创建步骤文档（每步 <30 行）

#### 阶段4：检查点与恢复
- 4.1 自动保存状态
- 4.2 实现恢复逻辑
- 4.3 添加重试机制

#### 阶段5：工作流自动化
- 5.1 封装 unified-publish.py
- 5.2 创建步骤编排器
- 5.3 添加日志系统

#### 阶段6：测试验证
- 6.1 模拟中断测试
- 6.2 上下文大小测试
- 6.3 端到端测试

### 验证目标
- SKILL.md 行数：< 100 行
- 单步骤 prompt：< 2K tokens
- 步骤遗漏率：0%
- 中断恢复时间：< 30 秒

### 状态：待处理
