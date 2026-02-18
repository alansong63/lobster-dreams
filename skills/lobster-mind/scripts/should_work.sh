#!/bin/bash
# 判断今天需不需要做 Lobster Mind 工作
# 触发时间: 2:00-3:00 (Dream 已在 1:00 完成)

STATE_FILE="$HOME/.openclaw/workspace/skills/lobster-mind/data/state.json"
mkdir -p "$(dirname $STATE_FILE)"

# 初始化状态文件
if [ ! -f "$STATE_FILE" ]; then
    echo '{"lastDreamDate": "", "lastSectionGenerated": "", "sectionOrder": ["thoughts", "ideas", "essays", "reflections", "lifestyle"], "sectionsDoneThisWeek": [], "lastWeeklyReport": "", "weeklySectionsDone": []}' > "$STATE_FILE"
fi

# 获取当前日期和时间
CURRENT_DATE=$(date +%Y-%m-%d)
WEEKDAY=$(date +%u)  # 1=Monday, 6=Saturday, 7=Sunday
HOUR=$(date +%H)

# 只在 2:00-3:00 时段触发（避免与 Dream 1:00 冲突）
if [ "$HOUR" != "02" ] && [ "$HOUR" != "03" ]; then
    echo "NO_WORK"
    exit 1
fi

# 每周六 (weekday=6): 生成周报
if [ "$WEEKDAY" = "6" ]; then
    LAST_REPORT=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('lastWeeklyReport',''))" 2>/dev/null)
    if [ "$LAST_REPORT" != "$CURRENT_DATE" ]; then
        echo "WEEKLY"
        exit 0
    fi
fi

# 日常: 生成其他 5 个板块中的 1 个
# 读取当前应该生成哪个板块
LAST_SECTION=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('lastSectionGenerated',''))" 2>/dev/null)
SECTION_ORDER='["thoughts", "ideas", "essays", "reflections", "lifestyle"]'

# 计算下一个板块
NEXT_SECTION=$(python3 -c "
import json
sections = json.loads('$SECTION_ORDER')
last_section = '$LAST_SECTION'
if last_section == '':
    print(sections[0])
else:
    try:
        idx = sections.index(last_section)
        print(sections[(idx + 1) % len(sections)])
    except:
        print(sections[0])
")

echo "SECTION:$NEXT_SECTION"
exit 0
