# 问题记录 - 2026-02-16

## 事件：Cron Job 重复通知问题

### 问题描述
从 10:25 开始，收到大量重复的 "dream-to-html" subagent 任务完成通知，每分钟 1-2 条，内容完全相同。

### 根本原因
"Sync to Lobstermind & lobster-dreams" cron job (id: 3df7758b-38db-4daa-8398-c98481f2beec) 的 delivery 配置出错。

错误信息：`Delivering to Feishu requires target <chatId|user:openId|chat:chatId>`

该 cron job 在 10:04-11:08 期间不断失败重试，导致重复通知。

### 解决措施
- 已禁用该 cron job
- 计划：检查 delivery 配置后重新启用

### 待处理
- 检查飞书配置是否有变化
- 验证 cron job delivery 配置
- 重新启用 job 并测试
