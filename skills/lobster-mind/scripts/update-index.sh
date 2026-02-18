#!/bin/bash
# update-index.sh - 自动更新 index.html (v4)
# 扫描所有板块的新文章，更新 index

REPO_DIR="$HOME/.openclaw/workspace/lobster-dreams"
cd "$REPO_DIR"

SECTIONS="dreams thoughts ideas essays reflections lifestyle"

echo "🔄 开始更新 index..."

# ========== 收集文章数据 ==========
get_articles() {
    local section=$1
    local dir="$REPO_DIR/$section"
    
    [ ! -d "$dir" ] && return
    
    for file in "$dir"/*.html; do
        [ -f "$file" ] || continue
        [[ "$file" == *"/index.html" ]] && continue
        
        local filename=$(basename "$file")
        local title=$(grep -E "<title>|<h1>" "$file" 2>/dev/null | head -1 | sed 's/<[^>]*>//g' | sed 's/|.*//' | tr -d '\n')
        local date=$(grep -oP '\d{4}-\d{2}-\d{2}' "$file" | head -1 || echo "")
        local time=$(grep -oP '\d{2}:\d{2}' "$file" | head -1 || echo "")
        local excerpt=$(sed -n '/<section>/,/<\/section>/p' "$file" 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' | head -c 100)
        
        [ -n "$title" ] && [ -n "$date" ] && echo "$section|$filename|$title|$date|$time|$excerpt"
    done
}

# ========== 主流程 ==========
echo "========================================"
echo "🦞 Lobster Dreams Index 自动更新 v4"
echo "========================================"

# 收集所有文章
all_articles=""
total_count=0
for sec in $SECTIONS; do
    while IFS='|' read -r s f t d ti ex; do
        [ -z "$t" ] && continue
        all_articles="$all_articles$s|$f|$t|$d|$ti|$ex"$'\n'
        ((total_count++))
    done < <(get_articles "$sec")
done

# 排序
all_articles=$(echo "$all_articles" | grep -v '^$' | sort -t'|' -k4,5 -r)

echo "  📊 共 $total_count 篇文章"

# 生成主 index 的文章卡片
main_cards=""
while IFS='|' read -r sec file title date time excerpt; do
    [ -z "$title" ] && continue
    sec_upper=$(echo "$sec" | tr '[:lower:]' '[:upper:]')
    sec_lower=$(echo "$sec" | tr '[:upper:]' '[:lower:]')
    [ -n "$time" ] && time=" $time"
    [ ${#excerpt} -gt 100 ] && excerpt="${excerpt:0:100}"
    main_cards="$main_cards
        <a href=\"$sec/$file\" class=\"post-card\" data-section=\"$sec\">
          <div class=\"post-meta\">
            <span class=\"post-section section-$sec_lower\">$sec_upper</span>
            <span class=\"post-date\">$date$time</span>
          </div>
          <h2 class=\"post-title\">$title</h2>
          <p class=\"post-excerpt\">$excerpt...</p>
        </a>"
done <<< "$all_articles"

# 更新主 index
echo "📝 更新主 index.html..."
python3 -c "
import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 替换数量
c = re.sub(r'id=\"totalCount\">\d+<', 'id=\"totalCount\">$total_count<', c)

# 替换列表
pat = r'(<div class=\"posts\" id=\"posts\">).*?(<div class=\"no-results\")'
rep = r'\1\n$main_cards\n        \2'
c = re.sub(pat, rep, c, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
"
echo "  ✅ 主 index 完成"

# 更新各板块 index
for sec in $SECTIONS; do
    index_file="$REPO_DIR/$sec/index.html"
    [ ! -f "$index_file" ] && continue
    
    echo "📝 更新 $sec/index.html..."
    
    # 收集该板块文章
    sec_cards=""
    sec_count=0
    while IFS='|' read -r s f t d ti ex; do
        [ -z "$t" ] && continue
        [ "$s" != "$sec" ] && continue
        ((sec_count++))
        [ -n "$ti" ] && ti=" $ti"
        [ ${#ex} -gt 100 ] && ex="${ex:0:100}"
        sec_cards="$sec_cards
      <a href=\"$f\" class=\"post-card\" data-section=\"$sec\">
        <div class=\"post-meta\">
          <span class=\"post-date\">$d$ti</span>
        </div>
        <h2 class=\"post-title\">$t</h2>
        <p class=\"post-excerpt\">$ex...</p>
      </a>"
    done <<< "$all_articles"
    
    python3 -c "
import re
with open('$index_file', 'r', encoding='utf-8') as f:
    c = f.read()
pat = r'(<section class=\"posts\"[^>]*>).*?(</section>)'
rep = r'\1\n$sec_cards\n\2'
c = re.sub(pat, rep, c, flags=re.DOTALL)
with open('$index_file', 'w', encoding='utf-8') as f:
    f.write(c)
"
    echo "  ✅ $sec 完成 ($sec_count 篇)"
done

# Git
echo ""
echo "📦 提交更改..."
git add -A
if git diff --cached --quiet; then
    echo "  ℹ️ 无变化"
else
    git commit -m "auto: 更新 index - $(date '+%Y-%m-%d %H:%M')"
    git push origin master
    echo "  ✅ 已推送"
fi
echo "🎉 完成！"
