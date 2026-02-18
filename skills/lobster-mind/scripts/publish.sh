#!/bin/bash
# 发布内容到 GitHub

REPO_DIR="$HOME/.openclaw/workspace/lobster-dreams"

if [ ! -d "$REPO_DIR" ]; then
    echo "Error: Repository not found at $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR"

# 添加所有更改
git add -A

# 检查是否有更改
if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# 提交（标题作为参数）
TITLE="${1:-"chore: update content"}"
git commit -m "$TITLE"

# 推送到远程
echo "Publishing to GitHub..."
git push origin master

echo "✅ Published successfully"
