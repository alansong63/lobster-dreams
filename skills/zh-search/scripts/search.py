#!/usr/bin/env python3
"""
中文搜索包装器 - 调用 baidu-search
"""
import sys
import os

# baidu-search 脚本路径
workspace = os.path.expanduser("~/.openclaw/workspace")
baidu_search_script = os.path.join(
    workspace,
    "skills",
    "baidu-search",
    "scripts",
    "search.py"
)

# 执行 baidu-search
if __name__ == "__main__":
    import subprocess
    result = subprocess.run(
        [sys.executable, baidu_search_script] + sys.argv[1:],
        capture_output=False
    )
    sys.exit(result.returncode)
