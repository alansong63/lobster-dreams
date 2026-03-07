# 文清 - DOCX 文件读取指南

## 问题背景
文清（飞书 clerk 角色）无法直接读取 .docx 文件。

## 解决方案

### 方法 1：使用 pandoc 转换为 Markdown（推荐）

最简单的读取方式，适合只需要提取文字内容的场景：

```bash
pandoc --track-changes=all 文件.docx -o 输出.md
```

然后读取生成的 `.md` 文件即可。

### 方法 2：使用 Anthropic 官方 docx 技能

完整技能已复制到：`~/.openclaw/workspace/skills/feishu-clerk/docx/SKILL.md`

**核心流程：**

1. **解包 DOCX**
```bash
python scripts/office/unpack.py 文件.docx unpacked/
```

2. **读取 XML**
- 文字内容在 `unpacked/word/document.xml`
- 用文本编辑器或 `cat` 查看

3. **打包（如需要修改后）**
```bash
python scripts/office/pack.py unpacked/ 输出.docx --original 文件.docx
```

### 快速脚本

创建一个简单的读取脚本 `read-docx.sh`：

```bash
#!/bin/bash
# read-docx.sh - 快速读取 DOCX 文件

if [ -z "$1" ]; then
    echo "用法：./read-docx.sh 文件.docx"
    exit 1
fi

DOCX_FILE="$1"
TEMP_DIR=$(mktemp -d)

# 解包
python scripts/office/unpack.py "$DOCX_FILE" "$TEMP_DIR"

# 提取主要文字（简单 grep）
grep -oP '(?<=<w:t[^>]*>)[^<]+' "$TEMP_DIR/word/document.xml"

# 清理
rm -rf "$TEMP_DIR"
```

## 依赖安装

```bash
# pandoc
sudo apt install pandoc  # Ubuntu/Debian
brew install pandoc      # macOS

# Python 脚本依赖（通常已包含）
pip install lxml
```

## 技能位置

- 完整技能：`~/.openclaw/workspace/skills/feishu-clerk/docx/SKILL.md`
- 脚本工具：`~/.openclaw/workspace/skills/feishu-clerk/docx/scripts/`

---

**注意：** 临时下载的原始技能在 `~/.openclaw/workspace/anthropic-skills-temp/skills/docx/`，用完后可以删除。
