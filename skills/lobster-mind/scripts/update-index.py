#!/usr/bin/env python3
"""
update-index.py - 自动更新 index.html
扫描所有板块的新文章，更新主 index 和各板块 index
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

REPO_DIR = Path("/home/ubuntu/.openclaw/workspace/lobster-dreams")
SECTIONS = ["dreams", "thoughts", "ideas", "essays", "reflections", "lifestyle"]

def collect_articles(section: str) -> list:
    """收集指定板块的所有文章"""
    dir_path = REPO_DIR / section
    if not dir_path.exists():
        return []
    
    articles = []
    for html_file in dir_path.glob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            content = html_file.read_text(encoding="utf-8")
            
            # 获取标题
            title_match = re.search(r"<title>([^<-]+)", content)
            if not title_match:
                title_match = re.search(r"<h1>([^<]+)", content)
            title = title_match.group(1).strip() if title_match else ""
            
            # 获取日期（支持 2026-02-14 或 2026.02.14 格式）
            date_match = re.search(r"(\d{4}[-.\}]\d{2}[-.\}]\d{2})", content)
            date = date_match.group(1).replace('.', '-') if date_match else ""
            
            # 标准化日期格式为 YYYY-MM-DD 用于排序
            date_for_sort = date.replace('-', '').replace('.', '') if date else ""
            
            # 获取时间
            time_match = re.search(r"\d{2}:\d{2}", content)
            time = time_match.group(0) if time_match else ""
            
            # 获取内容 - 全文（非摘要）
            content_text = ""
            # 尝试从 <div class="content"> 提取
            content_match = re.search(r'<div class="content">(.*?)</div>', content, re.DOTALL)
            if content_match:
                content_text = content_match.group(1)
            else:
                # 尝试从 <article> 提取
                article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
                if article_match:
                    content_text = article_match.group(1)
            
            # 清理 HTML 标签，获取纯文本
            content_text = re.sub(r'<[^>]+>', '', content_text)
            content_text = " ".join(content_text.split())  # 规范化空白
            
            if title and date:
                articles.append({
                    "section": section,
                    "file": html_file.name,
                    "title": title,
                    "date": date,
                    "date_sort": date_for_sort + time.replace(':', ''),
                    "time": time,
                    "excerpt": content_text  # 存储全文
                })
        except Exception as e:
            print(f"  ⚠️ 读取 {html_file} 失败: {e}")
    
    return articles

def generate_card(article: dict, show_section: bool = True) -> str:
    """生成文章卡片 HTML"""
    sec = article["section"]
    sec_upper = sec.upper()
    sec_lower = sec.lower()
    # 标准化日期显示格式
    display_date = article["date"].replace('-', '.')
    time = f" {article['time']}" if article['time'] else ""
    full_text = article.get('excerpt', '')
    
    # 首页显示摘要，板块页显示全文
    if show_section:
        # 首页：摘要（截断到150字符）
        excerpt = full_text[:150] + "..." if len(full_text) > 150 else full_text
    else:
        # 板块页：全文
        excerpt = full_text
    
    if show_section:
        return f"""        <a href="{sec}/{article['file']}" class="post-card" data-section="{sec}">
          <div class="post-meta">
            <span class="post-section section-{sec_lower}">{sec_upper}</span>
            <span class="post-date">{display_date}{time}</span>
          </div>
          <h2 class="post-title">{article['title']}</h2>
          <p class="post-excerpt">{excerpt}</p>
        </a>"""
    else:
        display_date = article["date"].replace('-', '.')
        return f"""      <a href="{article['file']}" class="post-card" data-section="{sec}">
        <div class="post-meta">
          <span class="post-date">{display_date}{time}</span>
        </div>
        <h2 class="post-title">{article['title']}</h2>
        <p class="post-excerpt">{excerpt}</p>
      </a>"""

def update_main_index(articles: list):
    """更新主 index.html"""
    print("📝 更新主 index.html...")
    
    index_file = REPO_DIR / "index.html"
    content = index_file.read_text(encoding="utf-8")
    
    # 按日期时间排序
    sorted_articles = sorted(articles, key=lambda x: x.get("date_sort", ""), reverse=True)
    
    # 生成卡片
    cards = "\n".join(generate_card(a) for a in sorted_articles)
    
    # 替换文章数量
    content = re.sub(r'id="totalCount">\d+<', f'id="totalCount">{len(sorted_articles)}<', content)
    
    # 替换文章列表
    pattern = r'(<div class="posts" id="posts">).*?(<div class="no-results")'
    replacement = r'\1\n' + cards + r'\n        \2'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    index_file.write_text(content, encoding="utf-8")
    print(f"  ✅ 完成 ({len(sorted_articles)} 篇)")

def update_section_index(section: str, articles: list):
    """更新各板块 index.html"""
    index_file = REPO_DIR / section / "index.html"
    if not index_file.exists():
        return
    
    print(f"📝 更新 {section}/index.html...")
    
    content = index_file.read_text(encoding="utf-8")
    
    # 筛选该板块文章
    section_articles = [a for a in articles if a["section"] == section]
    section_articles = sorted(section_articles, key=lambda x: (x["date"], x["time"]), reverse=True)
    
    # 生成卡片（不带板块标签）
    cards = "\n".join(generate_card(a, show_section=False) for a in section_articles)
    
    # 替换文章列表
    pattern = r'(<section class="posts"[^>]*>).*?(</section>)'
    replacement = r'\1\n' + cards + r'\n\2'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    index_file.write_text(content, encoding="utf-8")
    print(f"  ✅ {section} 完成 ({len(section_articles)} 篇)")

def main():
    print("========================================")
    print("🦞 Lobster Dreams Index 自动更新")
    print("========================================")
    
    # 收集所有文章
    all_articles = []
    for sec in SECTIONS:
        articles = collect_articles(sec)
        all_articles.extend(articles)
        print(f"  📂 {sec}: {len(articles)} 篇")
    
    print(f"  📊 共 {len(all_articles)} 篇文章")
    
    # 更新主 index
    update_main_index(all_articles)
    
    # 更新各板块 index
    for sec in SECTIONS:
        update_section_index(sec, all_articles)
    
    # Git 提交推送
    print("\n📦 提交更改...")
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    if subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True).returncode == 0:
        print("  ℹ️ 无变化")
    else:
        msg = f"auto: 更新 index - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], capture_output=True)
        subprocess.run(["git", "push", "origin", "master"], capture_output=True)
        print("  ✅ 已推送")
    
    print("\n🎉 完成！")

if __name__ == "__main__":
    main()
