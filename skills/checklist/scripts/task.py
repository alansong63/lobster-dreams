#!/usr/bin/env python3
"""
Checklist Task Manager - 任务 CRUD 操作
"""

import os
import json
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
CHECKLIST_DIR = Path.home() / ".openclaw" / "workspace" / ".checklist"
TASKS_DIR = CHECKLIST_DIR / "tasks"

# 确保目录存在
TASKS_DIR.mkdir(parents=True, exist_ok=True)


def _get_task_path(task_id: str) -> Path:
    """获取任务文件路径"""
    return TASKS_DIR / f"{task_id}.json"


def create_task(title: str, steps: List[str] = None, metadata: Dict = None) -> str:
    """
    创建新任务
    
    Args:
        title: 任务标题
        steps: 步骤列表（默认 6 步）
        metadata: 额外元数据
    
    Returns:
        task_id
    """
    # 默认 6 步
    if steps is None:
        steps = [
            "需求定义 - 要做什么？",
            "研发目标 - 做到什么程度？",
            "执行计划 - 怎么做？",
            "实施执行 - 具体实现",
            "自检验证 - 做完了吗？",
            "完成交付 - 结束"
        ]
    
    task_id = f"task-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4]}"
    
    task_data = {
        "id": task_id,
        "title": title,
        "status": "pending",  # pending, in_progress, completed, paused
        "created": datetime.datetime.now().isoformat(),
        "updated": datetime.datetime.now().isoformat(),
        "progress": {
            "total": len(steps),
            "completed": 0,
            "percentage": 0,
            "current_step": 0
        },
        "steps": [
            {
                "id": i + 1,
                "content": step,
                "status": "pending"  # pending, in_progress, completed
            }
            for i, step in enumerate(steps)
        ],
        "logs": [
            {
                "time": datetime.datetime.now().isoformat(),
                "action": "创建任务",
                "detail": title
            }
        ],
        "metadata": metadata or {}
    }
    
    # 保存到文件
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task_data, f, indent=2, ensure_ascii=False)
    
    return task_id


def get_task(task_id: str) -> Optional[Dict]:
    """
    获取任务详情
    
    Args:
        task_id: 任务 ID
    
    Returns:
        任务数据字典，不存在返回 None
    """
    task_path = _get_task_path(task_id)
    if not task_path.exists():
        return None
    
    with open(task_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_task(task_id: str, data: Dict) -> bool:
    """
    更新任务
    
    Args:
        task_id: 任务 ID
        data: 要更新的数据
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 合并数据
    task.update(data)
    task['updated'] = datetime.datetime.now().isoformat()
    
    # 保存
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


def delete_task(task_id: str) -> bool:
    """
    删除任务
    
    Args:
        task_id: 任务 ID
    
    Returns:
        是否成功
    """
    task_path = _get_task_path(task_id)
    if not task_path.exists():
        return False
    
    task_path.unlink()
    return True


def list_tasks(status: str = None) -> List[Dict]:
    """
    列出所有任务
    
    Args:
        status: 过滤状态（pending, in_progress, completed, paused）
    
    Returns:
        任务列表
    """
    tasks = []
    
    for task_file in TASKS_DIR.glob("*.json"):
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
            if status is None or task.get('status') == status:
                tasks.append(task)
    
    # 按更新时间排序
    tasks.sort(key=lambda x: x.get('updated', ''), reverse=True)
    
    return tasks


def update_task_status(task_id: str, status: str) -> bool:
    """
    更新任务状态
    
    Args:
        task_id: 任务 ID
        status: 新状态（pending, in_progress, completed, paused）
    
    Returns:
        是否成功
    """
    return update_task(task_id, {"status": status})


def complete_step(task_id: str, step_id: int = None) -> bool:
    """
    完成步骤
    
    Args:
        task_id: 任务 ID
        step_id: 步骤 ID（默认当前步骤）
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    steps = task.get('steps', [])
    progress = task.get('progress', {})
    
    # 如果没有指定 step_id，默认完成当前步骤
    if step_id is None:
        step_id = progress.get('current_step', 0) + 1
    
    # 找到步骤并标记完成
    for step in steps:
        if step['id'] == step_id:
            step['status'] = 'completed'
            break
    
    # 更新进度
    completed_count = sum(1 for s in steps if s['status'] == 'completed')
    progress['completed'] = completed_count
    progress['percentage'] = int(completed_count / len(steps) * 100) if steps else 0
    progress['current_step'] = completed_count
    
    # 如果全部完成，更新任务状态
    if completed_count == len(steps):
        task['status'] = 'completed'
    
    # 添加日志
    task['logs'].append({
        "time": datetime.datetime.now().isoformat(),
        "action": "完成步骤",
        "detail": f"步骤 {step_id} 已完成"
    })
    
    task['updated'] = datetime.datetime.now().isoformat()
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


# 测试
if __name__ == "__main__":
    # 测试创建任务
    task_id = create_task("测试 Checklist 0.4.0")
    print(f"创建任务: {task_id}")
    
    # 测试获取任务
    task = get_task(task_id)
    print(f"任务详情: {task['title']}, 状态: {task['status']}")
    
    # 测试列出任务
    tasks = list_tasks()
    print(f"总任务数: {len(tasks)}")
