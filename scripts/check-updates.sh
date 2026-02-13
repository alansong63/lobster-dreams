#!/bin/bash
# 检查 OpenClaw 和相关插件的更新

CHECK_DIR="$HOME/.openclaw/workspace"
STATE_FILE="$CHECK_DIR/.update-check-state.json"
LOG_FILE="$CHECK_DIR/logs/update-check.log"

# 创建目录
mkdir -p "$(dirname "$STATE_FILE")"
mkdir -p "$(dirname "$LOG_FILE")"

# 加载或初始化状态
load_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo '{}'
    fi
}

save_state() {
    echo "$1" > "$STATE_FILE"
}

# 检查 GitHub release 版本
check_github_release() {
    local repo=$1
    local name=$2
    local current=$3

    echo "Checking $name..." >> "$LOG_FILE"

    # 获取最新版本
    local latest=$(curl -s "https://api.github.com/repos/$repo/releases/latest" | grep -o '"tag_name": *"[^"]*"' | cut -d'"' -f4)

    if [ -z "$latest" ]; then
        echo "  Failed to fetch latest version for $name" >> "$LOG_FILE"
        return
    fi

    echo "  Current: $current, Latest: $latest" >> "$LOG_FILE"

    if [ "$current" != "$latest" ]; then
        return 1  # 有更新
    fi
    return 0
}

# 记录日志
echo "=== Update check $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 加载之前的状态
STATE=$(load_state)

# 检查各个项目
UPDATES=""

# 1. OpenClaw
CURRENT_OPENCLAW=$(openclaw --version 2>/dev/null || openclaw version 2>/dev/null || echo "unknown")
if ! check_github_release "openclaw/openclaw" "OpenClaw" "$CURRENT_OPENCLAW"; then
    UPDATES="$UPDATES\n🦞 OpenClaw: $CURRENT_OPENCLAW → $(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" | grep -o '"tag_name": *"[^"]*"' | cut -d'"' -f4)"
fi

# 2. OpenCode
CURRENT_OPENCODE=$(opencode --version 2>/dev/null || echo "unknown")
if ! check_github_release "anomalyco/opencode" "OpenCode" "$CURRENT_OPENCODE"; then
    UPDATES="$UPDATES\n💻 OpenCode: $CURRENT_OPENCODE → $(curl -s "https://api.github.com/repos/anomalyco/opencode/releases/latest" | grep -o '"tag_name": *"[^"]*"' | cut -d'"' -f4)"
fi

# 3. Feishu Extension (检查目录是否存在)
if [ -d "$HOME/.openclaw/extensions/feishu" ]; then
    # 从 package.json 获取版本
    CURRENT_FEISHU=$(cat "$HOME/.openclaw/extensions/feishu/package.json" 2>/dev/null | grep -o '"version": *"[^"]*"' | cut -d'"' -f4 || echo "unknown")
    # Feishu 扩展可能在 openclaw 仓库里，也可能在独立仓库
    # 这里先简单处理，如果需要可以更新
    echo "Feishu extension found: $CURRENT_FEISHU" >> "$LOG_FILE"
fi

# 4. Superpowers (opencode skills)
if [ -d "$HOME/.config/opencode/superpowers" ]; then
    cd "$HOME/.config/opencode/superpowers"
    LATEST_COMMIT=$(git fetch origin 2>/dev/null && git rev-parse origin/main 2>/dev/null)
    CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null)
    if [ "$CURRENT_COMMIT" != "$LATEST_COMMIT" ]; then
        UPDATES="$UPDATES\n⚡ Superpowers: 有新提交 (使用 'cd ~/.config/opencode/superpowers && git pull' 更新)"
    fi
fi

# 5. Code-Documenter skill
if [ -d "$HOME/.agents/skills/code-documenter" ]; then
    echo "Code-Documenter skill installed" >> "$LOG_FILE"
fi

# 如果有更新，发送提醒
if [ -n "$UPDATES" ]; then
    echo "发现更新:" >> "$LOG_FILE"
    echo "$UPDATES" >> "$LOG_FILE"

    # 使用 openclaw 发送提醒（如果可用）
    if command -v openclaw &> /dev/null; then
        echo "🔔 发现更新！
$UPDATES

检查日志: $LOG_FILE" | openclaw gateway wake --mode now 2>/dev/null || true
    fi
else
    echo "所有项目都是最新版本" >> "$LOG_FILE"
fi

echo "================================" >> "$LOG_FILE"
