#!/usr/bin/env python3
"""
Checklist Converter - JSON → MD 转换
将任务 JSON 转换为可读的 MD 格式
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Optional
try:
    from .task import get_task, TASKS_DIR
except ImportError:
    from task import get_task, TASKS_DIR


def get_md_path(task_id: str) -> Path:
    """获取 MD 文件路径"""
    return TASKS_DIR / f"{task_id}.md"


def json_to_md(task_id: str, force: bool = False) -> Optional[str]:
    """
    将任务 JSON 转换为 MD 格式
    
    Args:
        task_id: 任务 ID
        force: 是否强制重新生成
    
    Returns:
        MD 文件路径，失败返回 None
    """
    task = get_task(task_id)
    if not task:
        return None
    
    md_path = get_md_path(task_id)
    
    # 如果文件存在且不强制重新生成，跳过
    if md_path.exists() and not force:
        return str(md_path)
    
    # 生成 MD 内容
    md_content = _generate_md_content(task)
    
    # 写入文件
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return str(md_path)


def _generate_md_content(task: Dict) -> str:
    """生成 MD 内容"""
    
    # 状态 emoji
    status_emoji = {
        "pending": "⏳ 待处理",
        "in_progress": "🔄 进行中",
        "completed": "✅ 已完成",
        "paused": "⏸️ 已暂停"
    }
    
    status = task.get('status', 'pending')
    progress = task.get('progress', {})
    steps = task.get('steps', [])
    logs = task.get('logs', [])
    decisions = task.get('decisions', [])
    problems = task.get('problems', [])
    
    lines = []
    
    # 标题
    lines.append(f"# 任务：{task.get('title', 'Untitled')}")
    lines.append("")
    
    # 基本信息
    lines.append("## 📌 基本信息")
    lines.append("")
    lines.append(f"- **ID**: `{task.get('id')}`")
    lines.append(f"- **状态**: {status_emoji.get(status, status)}")
    lines.append(f"- **进度**: {progress.get('percentage', 0)}% ({progress.get('completed', 0)}/{progress.get('total', 0)})")
    lines.append(f"- **创建时间**: {task.get('created', '')[:19].replace('T', ' ')}")
    lines.append(f"- **更新时间**: {task.get('updated', '')[:19].replace('T', ' ')}")
    lines.append("")
    
    # 步骤进度
    lines.append("## 📋 执行计划")
    lines.append("")
    for step in steps:
        step_status = step.get('status', 'pending')
        if step_status == 'completed':
            checkbox = "[x]"
            emoji = "✅"
        elif step_status == 'in_progress':
            checkbox = "[ ]"
            emoji = "🔄"
        else:
            checkbox = "[ ]"
            emoji = "⬜"
        
        lines.append(f"- {checkbox} {step.get('id')}. {step.get('content', '')} {emoji}")
    lines.append("")
    
    # 关键决策
    if decisions:
        lines.append("## 💡 关键决策")
        lines.append("")
        lines.append("| 时间 | 决策 | 理由 |")
        lines.append("|------|------|------|")
        for d in decisions:
            time = d.get('time', '')[:16].replace('T', ' ')
            decision = d.get('decision', '')
            reason = d.get('reason', '')
            lines.append(f"| {time} | {decision} | {reason} |")
        lines.append("")
    
    # 问题与解决
    if problems:
        lines.append("## 🔧 问题与解决")
        lines.append("")
        for p in problems:
            problem = p.get('problem', '')
            solution = p.get('solution', '')
            if solution:
                lines.append(f"### ❓ {problem}")
                lines.append(f"- **解决**: {solution}")
                lines.append("")
            else:
                lines.append(f"### ❓ {problem}")
                lines.append("")
    
    # 执行日志
    if logs:
        lines.append("## 📝 执行日志")
        lines.append("")
        
        # 按时间倒序显示最近10条
        recent_logs = logs[-10:] if len(logs) > 10 else logs
        for log in recent_logs:
            time = log.get('time', '')[:16].replace('T', ' ')
            action = log.get('action', '')
            detail = log.get('detail', '')
            lines.append(f"### {time}")
            lines.append(f"- **{action}**: {detail}")
            lines.append("")
    
    # 下一步
    lines.append("## 📌 下一步")
    lines.append("")
    
    # 找到当前进行中的步骤
    current_step = progress.get('current_step', 0)
    next_step = None
    for step in steps:
        if step.get('status') == 'in_progress':
            next_step = step
            break
    
    if next_step:
        lines.append(f"- [ ] {next_step.get('id')}. {next_step.get('content', '')}")
    elif current_step < len(steps):
        next_step = steps[current_step]
        lines.append(f"- [ ] {next_step.get('id')}. {next_step.get('content', '')}")
    
    lines.append("")
    
    return "\n".join(lines)


def sync_md(task_id: str) -> Optional[str]:
    """
    同步更新 MD 存档（强制重新生成）
    
    Args:
        task_id: 任务 ID
    
    Returns:
        MD 文件路径
    """
    return json_to_md(task_id, force=True)


def read_md(task_id: str) -> Optional[str]:
    """
    读取任务的 MD 存档
    
    Args:
        task_id: 任务 ID
    
    Returns:
        MD 内容，不存在返回 None
    """
    md_path = get_md_path(task_id)
    if not md_path.exists():
        # 如果不存在，生成一下
        json_to_md(task_id)
    
    if md_path.exists():
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None


def delete_md(task_id: str) -> bool:
    """
    删除任务的 MD 存档
    
    Args:
        task_id: 任务 ID
    
    Returns:
        是否成功
    """
    md_path = get_md_path(task_id)
    if md_path.exists():
        md_path.unlink()
        return True
    return False


# 测试
if __name__ == "__main__":
    from .task import create_task
    
    # 测试创建任务
    task_id = create_task("测试 Converter")
    print(f"创建任务: {task_id}")
    
    # 测试生成 MD
    md_path = json_to_md(task_id)
    print(f"MD 路径: {md_path}")
    
    # 测试读取 MD
    md_content = read_md(task_id)
    print("\n=== MD 内容 ===")
    print(md_content)
