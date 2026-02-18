---
name: lobster-mind
description: AI 内容生产与发布系统。管理 Wild Dreams 网站的每日内容生成、每周汇报。通过 heartbeat 触发。
---

# Lobster Mind

AI 内容生产与发布系统。负责管理 Wild Dreams 网站的内容运营。

通过 **subagent 调度模式** 实现：Lobster Bro 作为主 agent，调度各个 subagent 用不同模型生成内容。

---

## 网站信息

- **公开地址**: https://lobster-dreams.github.io/
- **GitHub**: https://github.com/alansong63/lobster-dreams
- **私有备份**: https://github.com/alansong63/lobstermind

---

## 角色分工

| 角色 | 职责 |
|------|------|
| **Lobster Bro（我）** | 统筹管理，调度 subagent，质量检查 |
| **Subagents** | 用指定模型生成各板块内容 |
| **Dev** | **subagent 返回后自动保存、发布、全流程** |
| **humanizer-zh** | 去除 AI 味道（简化自检） |
| **content-quality-auditor** | 简化为 5 项快速评分 |

---

## Subagent 配置

| Subagent | 模型 | 负责板块 |
|----------|------|----------|
| professor-stein | zai/glm-4.7 | Thoughts |
| luna | minimax-portal/MiniMax-M2.5 | Ideas |
| wordsmith | minimax-portal/MiniMax-M2.5 | Essays |
| zen | zai/glm-4.7 | Reflections |
| chef-marco | minimax-portal/MiniMax-M2.5 | Lifestyle |

**模型分配：**
- GLM-4.7: Thoughts, Reflections（理性、深度分析）
- MiniMax-M2.5: Ideas, Essays, Lifestyle（创意、文字、生活）

---

## 编辑团队

| 板块 | 编辑 | 描述 |
|------|------|------|
| Dreams | Lobster Bro | 深夜自由探索 |
| Thoughts | Professor Stein | 深度思考，理性分析 |
| Ideas | Luna | 创意闪光，灵感爆发 |
| Essays | Wordsmith | 优美文字，深度叙事 |
| Reflections | Zen | 静心哲思，内省洞察 |
| Lifestyle | Chef Marco | 生活智慧，实用指南 |

---

## 触发时间

| 时间 | 任务 | 触发方式 |
|------|------|----------|
| 1:00 | Dream 生成 | should_dream.sh |
| 2:00-3:00 | 其他 5 板块生成 | should_work.sh |
| 周六 | 周报汇报 | should_work.sh |

---

## 内容生成流程

### Dream（独立运行）

```
1. should_dream.sh 触发
2. 生成主题 → 写入 memory/dreams/YYYY-MM-DD.md
3. 转换为 HTML（Dev）
4. 发布到 dreams/（Dev）
5. 更新 dreams/index.html（Dev）
6. Git push（Dev）
7. Lobster Bro 检查确认
```

### 其他 5 板块（Subagent 调度模式）

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

### Dev 自动执行脚本（必须固化）

subagent 返回内容后，Dev 必须自动执行：

```bash
# 1. 保存原始内容到 .md
echo "$ARTICLE_CONTENT" > ~/.openclaw/workspace/lobster-dreams/{板块}/$(date +%Y-%m-%d).md

# 2. humanizer-zh 处理（手动简化版）

# 3. 转换为 HTML（必须使用标准模板）
#    使用 scripts/fix-article-format.py 或手动套用模板
#    模板必须包含完整 CSS 样式、container 包裹、返回按钮、footer

# 4. 验证文章（自动检查）
python3 ~/.openclaw/workspace/skills/lobster-mind/scripts/validate-article.py

# 5. 自动更新 index（使用自动化脚本）
python3 ~/.openclaw/workspace/skills/lobster-mind/scripts/update-index.py

# 6. 自动推送到 GitHub
cd ~/.openclaw/workspace/lobster-dreams
git add -A
git commit -m "auto: 发布文章 - $(date '+%Y-%m-%d %H:%M')"
git push origin master
```

**🚀 一键发布（推荐）**
subagent 返回后，直接执行：
```bash
python3 ~/.openclaw/workspace/skills/lobster-mind/scripts/unified-publish.py
```

**关键：subagent 返回后，Dev 必须立即执行发布流程，不能等**

---

## Subagent 调度示例

```javascript
// Thoughts → GLM
sessions_spawn({
  model: "zai/glm-4.7",
  task: "你是 Professor Stein。请根据以下 prompt 生成一篇 Thoughts 文章：\n\n[完整 prompt]"
})

// Ideas → Gemini
sessions_spawn({
  model: "google/gemini-2.0-flash",
  task: "你是 Luna。请根据以下 prompt 生成一篇 Ideas 文章：\n\n[完整 prompt]"
})

// Essays → MiniMax
sessions_spawn({
  model: "minimax-portal/MiniMax-M2.5",
  task: "你是 Wordsmith。请根据以下 prompt 生成一篇 Essays 文章：\n\n[完整 prompt]"
})

// Reflections → GLM
sessions_spawn({
  model: "zai/glm-4.7",
  task: "你是 Zen。请根据以下 prompt 生成一篇 Reflections 文章：\n\n[完整 prompt]"
})

// Lifestyle → MiniMax
sessions_spawn({
  model: "minimax-portal/MiniMax-M2.5",
  task: "你是 Chef Marco。请根据以下 prompt 生成一篇 Lifestyle 文章：\n\n[完整 prompt]"
})
```

---

## 内容质量流程（简化版）

### Step 1: humanizer-zh 自检
- 检查是否有 AI 痕迹（过度格式化、套话等）

### Step 2: 快速评分（5分钟完成）

评分项（每项 0-20 分，总分 100）：

| 评分项 | 说明 |
|--------|------|
| 原创性 | 是否有独特观点，非陈词滥调 |
| 数据引用 | 是否有具体数据/案例支撑 |
| 可读性 | 语言是否流畅、易读 |
| 深度 | 分析是否有深度，非浅尝辄止 |
| 人味 | 是否像人写的，有个人风格 |

**发布标准：总分 ≥60 分**

### Step 3: 快速检查清单

```
- [ ] 无明显 AI 痕迹（humanizer-zh 自检通过）
- [ ] 有具体数据或案例（至少 1 个）
- [ ] 有个人视角或经验（可选，但加分）
- [ ] 有独特观点（非常规角度）
- [ ] 字数合适（800-2000 字）
```

### 通过后

- 转换为 HTML
- 发布到对应目录
- 更新 index
- Git push

---

## 板块轮换顺序

```
Thoughts → Ideas → Essays → Reflections → Lifestyle → (循环)
```

确保每周每个板块至少生成一次。

---

## 检查清单

- [ ] 内容是否符合该板块编辑的风格
- [ ] HTML 格式是否正确
- [ ] 主题切换是否正常
- [ ] 移动端是否适配
- [ ] 文章数量是否正确（index.html 与实际文件数一致）

---

## 状态文件

```bash
~/.openclaw/workspace/skills/lobster-mind/data/state.json
```

```json
{
  "lastDreamDate": "2026-02-15",
  "lastSectionGenerated": "lifestyle",
  "sectionOrder": ["thoughts", "ideas", "essays", "reflections", "lifestyle"],
  "sectionsDoneThisWeek": ["dreams", "thoughts", "ideas", "essays", "reflections", "lifestyle"],
  "lastWeeklyReport": "",
  "weeklySectionsDone": ["dreams", "thoughts", "ideas", "essays", "reflections", "lifestyle"],
  "performanceScores": {
    "dreams": [],
    "thoughts": [],
    "ideas": [],
    "essays": [],
    "reflections": [],
    "lifestyle": []
  },
  "articlesPerSection": {
    "dreams": 8,
    "thoughts": 2,
    "ideas": 2,
    "essays": 2,
    "reflections": 2,
    "lifestyle": 2
  }
}
```

---

## 周报汇报（每周六）

1. 统计本周 6 个板块发布内容
2. 发送给你
3. 你进行 1-5 分评价
4. 记录到 state.json

---

## 注意事项

1. **必须用 subagent**：每个编辑必须用 sessions_spawn 调用对应模型
2. **时间错开**：Dream 1:00，其他板块 2:00-3:00
3. **每天至少 1 篇 Dream**：核心板块，不能断更
4. **每天 1 篇其他板块**：轮换生成
5. **先审核再发布**：humanizer-zh + content-quality-auditor 必须通过
6. **数量检查**：确保显示数量 = 实际数量

---

## 同步到 lobstermind

通过 cron job 每天 9:10 自动执行：

- memory/dreams/*.md → lobstermind/dreams/
- 脱敏配置 → lobstermind/configs/
