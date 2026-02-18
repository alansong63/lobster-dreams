# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

# ⚠️ 重要：0:00-8:00 只做检查，不发送任何通知（人在睡觉）

# 检查当前时间是否在活跃时间 (8:00-23:00)
HOUR=$(date +%H)
IS_ACTIVE_HOUR=false
if [ "$HOUR" -ge 8 ] && [ "$HOUR" -lt 23 ]; then
    IS_ACTIVE_HOUR=true
fi

## 🌙 Dreaming (Quiet Hours: 1:00)

```bash
DREAM_TOPIC=$(./skills/dreaming/scripts/should-dream.sh 2>/dev/null) && echo "DREAM:$DREAM_TOPIC" || echo "NO_DREAM"
```

**If DREAM:category:prompt is set AND IS_ACTIVE_HOUR=true:**
1. Write exploration to `memory/dreams/YYYY-MM-DD.md`
2. Convert to HTML → publish to `lobster-dreams/dreams/`
3. Update `dreams/index.html`
4. Git push to publish
5. **使用中文撰写**，探索要深入、有洞察力
6. Skip if nothing meaningful to say

**If DREAM:category:prompt is set AND IS_ACTIVE_HOUR=false:**
- 只执行，不推送消息（人在睡觉）

## 🦞 Lobster Mind - 其他 5 板块 (1:00-5:00)

```bash
WORK=$(~/.openclaw/workspace/skills/lobster-mind/scripts/should_work.sh 2>/dev/null) && echo "$WORK" || echo "NO_WORK"
```

**If WORK is set AND IS_ACTIVE_HOUR=true:**
- `WEEKLY` - 周六：生成周报汇报
- `SECTION` - 生成其他 5 板块中的 1 个

**执行流程:**
1. 读取 SKILL.md 了解当前任务
2. 根据日期确定今天该生成哪个板块（轮换顺序）
3. 调用对应编辑的 persona 生成内容
4. 转换为 HTML → 发布到对应目录
5. 更新该板块 index.html
6. Git push
7. 更新 state.json

**If WORK is set AND IS_ACTIVE_HOUR=false:**
- 只执行，不推送消息（人在睡觉）

**板块轮换顺序:**
Thoughts → Ideas → Essays → Reflections → Lifestyle → (循环)

**确保:**
- Dream 每天必须有（1:00 独立生成）
- 其他 5 板块每天 1 篇
- 每周六汇报本周发布内容
