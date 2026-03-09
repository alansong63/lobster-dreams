# 插件安装 Checklist 模板 (宏观版)

> 适用于任何 OpenClaw 插件安装
>
> **版本**: 1.0.0 | **适用**: OpenClaw 插件安装 | **更新日期**: 2026-03-08

---

## 📋 安装前检查

```
[ ] 1. 确认插件来源
    ├── 官方插件 (@openclaw/xxx)
    ├── 社区插件 (ClawHub)
    └── 本地插件 (自研)

[ ] 2. 阅读插件文档
    ├── 功能简介
    ├── 配置项说明
    └── 依赖要求

[ ] 3. 评估兼容性
    ├── OpenClaw 版本要求
    ├── 依赖插件/技能
    └── 频道支持

[ ] 4. 准备回滚方案
    ├── 备份当前配置
    └── 记录安装步骤
```

---

## ⚙️ 安装执行

```
[ ] 5. 备份配置文件
    ├── openclaw.json
    └── 相关技能配置

[ ] 6. 执行安装
    ├── npm install / openclaw plugins install
    └── 确认安装成功

[ ] 7. 配置插件
    ├── 添加到 plugins.allow
    ├── 添加到 plugins.load.paths (如需要)
    ├── 配置 slots (如需要)
    └── 配置 entries (如需要)

[ ] 8. 验证配置
    ├── openclaw config validate
    └── 检查警告/错误
```

---

## ✅ 安装后验证

```
[ ] 9. 重启 Gateway
    ├── openclaw gateway restart
    └── 确认启动成功

[ ] 10. 功能测试
    ├── 测试核心功能
    ├── 测试边界情况
    └── 检查日志输出

[ ] 11. 监控稳定性
    ├── 运行 24-48 小时
    └── 观察内存/CPU/日志
```

---

## 🔄 回滚(如需要)

```
[ ] 12. 卸载插件
    ├── 移除 plugins 配置
    ├── 删除插件文件 (如需要)
    └── 重启 Gateway

[ ] 13. 恢复配置
    ├── 还原备份的配置文件
    └── 重启 Gateway
```

---

## 📊 快速复用

| 阶段 | 关键命令 |
|------|----------|
| 安装 | `openclaw plugins install <plugin>` |
| 验证 | `openclaw config validate` |
| 重启 | `openclaw gateway restart` |
| 查看日志 | `openclaw gateway logs -n 50` |
| 卸载 | 手动删除配置项 |

---

**版本**: 1.0.0
**适用**: OpenClaw 插件安装
