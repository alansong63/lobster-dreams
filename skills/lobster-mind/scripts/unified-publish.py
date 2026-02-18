#!/usr/bin/env python3
"""
unified-publish.py - 一键发布文章
自动执行：保存 → 模板 → 验证 → 更新 index → 推送
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

REPO_DIR = Path("/home/ubuntu/.openclaw/workspace/lobster-dreams")
SCRIPTS_DIR = Path("/home/ubuntu/.openclaw/workspace/skills/lobster-mind/scripts")

def run_script(script_path: Path, *args) -> bool:
    """运行脚本"""
    cmd = ["python3", str(script_path)]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_DIR)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ 脚本失败: {result.stderr}")
        return False
    return True

def git_commit_push(message: str) -> bool:
    """Git 提交推送"""
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    if subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True).returncode == 0:
        print("  ℹ️ 无变化需要提交")
        return True
    
    subprocess.run(["git", "commit", "-m", message], capture_output=True)
    result = subprocess.run(["git", "push", "origin", "master"], capture_output=True)
    
    if result.returncode == 0:
        print("  ✅ 已推送")
        return True
    else:
        print(f"  ❌ 推送失败: {result.stderr}")
        return False

def main():
    print("=" * 60)
    print("🦞 Wild Dreams 一键发布流程")
    print("=" * 60)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Step 1: 修复文章格式
    print("\n📝 Step 1: 修复文章格式...")
    if not run_script(SCRIPTS_DIR / "fix-article-format.py"):
        print("  ⚠️ 格式修复跳过或无新文章")
    
    # Step 2: 验证文章
    print("\n🔍 Step 2: 验证文章...")
    if (SCRIPTS_DIR / "validate-article.py").exists():
        if not run_script(SCRIPTS_DIR / "validate-article.py"):
            print("  ⚠️ 验证有警告，请检查")
    else:
        print("  ℹ️ 跳过验证（脚本不存在）")
    
    # Step 3: 更新 index
    print("\n📋 Step 3: 更新 index...")
    if not run_script(SCRIPTS_DIR / "update-index.py"):
        print("  ❌ index 更新失败")
        return
    
    # Step 4: Git 推送
    print("\n🚀 Step 4: 推送到 GitHub...")
    git_commit_push(f"auto: 发布文章 - {timestamp}")
    
    print("\n" + "=" * 60)
    print("🎉 全部完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
