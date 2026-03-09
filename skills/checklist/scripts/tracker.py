#!/usr/bin/env python3
"""
Checklist Tracker - 进度跟踪 + 钩子机制
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Callable, Optional
try:
    from .task import get_task, update_task, _get_task_path
except ImportError:
    from task import get_task, update_task, _get_task_path

# 钩子类型
HOOK_ON_TASK_START = "on_task_start"
HOOK_ON_STEP_COMPLETE = "on_step_complete"
HOOK_ON_TASK_COMPLETE = "on_task_complete"
HOOK_ON_TASK_PAUSE = "on_task_pause"
HOOK_ON_TASK_RESUME = "on_task_resume"

# 钩子注册表
_hooks: Dict[str, List[Callable]] = {
    HOOK_ON_TASK_START: [],
    HOOK_ON_STEP_COMPLETE: [],
    HOOK_ON_TASK_COMPLETE: [],
    HOOK_ON_TASK_PAUSE: [],
    HOOK_ON_TASK_RESUME: [],
}


def register_hook(hook_type: str, callback: Callable):
    """
    注册钩子
    
    Args:
        hook_type: 钩子类型
        callback: 回调函数
    """
    if hook_type in _hooks:
        _hooks[hook_type].append(callback)


def unregister_hook(hook_type: str, callback: Callable):
    """
    注销钩子
    
    Args:
        hook_type: 钩子类型
        callback: 回调函数
    """
    if hook_type in _hooks and callback in _hooks[hook_type]:
        _hooks[hook_type].remove(callback)


def trigger_hook(hook_type: str, task_data: Dict, extra: Dict = None):
    """
    触发钩子
    
    Args:
        hook_type: 钩子类型
        task_data: 任务数据
        extra: 额外数据
    """
    if hook_type not in _hooks:
        return
    
    context = {
        "task": task_data,
        "extra": extra or {},
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    for callback in _hooks[hook_type]:
        try:
            callback(context)
        except Exception as e:
            print(f"Hook error: {e}")


def log_action(task_id: str, action: str, detail: str = "") -> bool:
    """
    记录操作日志
    
    Args:
        task_id: 任务 ID
        action: 操作名称
        detail: 详细说明
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    log_entry = {
        "time": datetime.datetime.now().isoformat(),
        "action": action,
        "detail": detail
    }
    
    task['logs'].append(log_entry)
    task['updated'] = datetime.datetime.now().isoformat()
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


def update_progress(task_id: str, completed: int = None, percentage: int = None, current_step: int = None) -> bool:
    """
    更新进度
    
    Args:
        task_id: 任务 ID
        completed: 已完成步骤数
        percentage: 进度百分比
        current_step: 当前步骤
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    progress = task.get('progress', {})
    
    if completed is not None:
        progress['completed'] = completed
    if percentage is not None:
        progress['percentage'] = percentage
    if current_step is not None:
        progress['current_step'] = current_step
    
    # 自动计算百分比
    if completed is not None and 'total' in progress:
        progress['percentage'] = int(completed / progress['total'] * 100)
    
    task['progress'] = progress
    task['updated'] = datetime.datetime.now().isoformat()
    
    with open(_get_task_path(task_id), 'w', encoding='utf-2') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


def add_decision(task_id: str, decision: str, reason: str = "") -> bool:
    """
    记录关键决策
    
    Args:
        task_id: 任务 ID
        decision: 决策内容
        reason: 决策理由
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 初始化 decisions 列表
    if 'decisions' not in task:
        task['decisions'] = []
    
    decision_entry = {
        "time": datetime.datetime.now().isoformat(),
        "decision": decision,
        "reason": reason
    }
    
    task['decisions'].append(decision_entry)
    task['updated'] = datetime.datetime.now().isoformat()
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


def add_problem(task_id: str, problem: str, solution: str = "") -> bool:
    """
    记录问题与解决方案
    
    Args:
        task_id: 任务 ID
        problem: 问题描述
        solution: 解决方案
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 初始化 problems 列表
    if 'problems' not in task:
        task['problems'] = []
    
    problem_entry = {
        "time": datetime.datetime.now().isoformat(),
        "problem": problem,
        "solution": solution
    }
    
    task['problems'].append(problem_entry)
    task['updated'] = datetime.datetime.now().isoformat()
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    return True


def start_task(task_id: str) -> bool:
    """
    开始任务（触发 on_task_start 钩子）
    
    Args:
        task_id: 任务 ID
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 更新状态
    task['status'] = 'in_progress'
    task['started'] = datetime.datetime.now().isoformat()
    task['updated'] = datetime.datetime.now().isoformat()
    
    # 添加日志
    task['logs'].append({
        "time": datetime.datetime.now().isoformat(),
        "action": "开始任务",
        "detail": f"任务开始执行"
    })
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    # 触发钩子
    trigger_hook(HOOK_ON_TASK_START, task, {"action": "start"})
    
    return True


def complete_task(task_id: str) -> bool:
    """
    完成任务（触发 on_task_complete 钩子）
    
    Args:
        task_id: 任务 ID
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 更新状态
    task['status'] = 'completed'
    task['completed'] = datetime.datetime.now().isoformat()
    task['updated'] = datetime.datetime.now().isoformat()
    task['progress']['percentage'] = 100
    
    # 添加日志
    task['logs'].append({
        "time": datetime.datetime.now().isoformat(),
        "action": "完成任务",
        "detail": f"任务已完成"
    })
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    # 触发钩子
    trigger_hook(HOOK_ON_TASK_COMPLETE, task, {"action": "complete"})
    
    return True


def pause_task(task_id: str, reason: str = "") -> bool:
    """
    暂停任务（触发 on_task_pause 钩子）
    
    Args:
        task_id: 任务 ID
        reason: 暂停原因
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 更新状态
    task['status'] = 'paused'
    task['paused'] = datetime.datetime.now().isoformat()
    task['updated'] = datetime.datetime.now().isoformat()
    
    # 添加日志
    task['logs'].append({
        "time": datetime.datetime.now().isoformat(),
        "action": "暂停任务",
        "detail": reason or "任务暂停"
    })
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    # 触发钩子
    trigger_hook(HOOK_ON_TASK_PAUSE, task, {"reason": reason})
    
    return True


def resume_task(task_id: str) -> bool:
    """
    恢复任务（触发 on_task_resume 钩子）
    
    Args:
        task_id: 任务 ID
    
    Returns:
        是否成功
    """
    task = get_task(task_id)
    if not task:
        return False
    
    # 更新状态
    task['status'] = 'in_progress'
    task['resumed'] = datetime.datetime.now().isoformat()
    task['updated'] = datetime.datetime.now().isoformat()
    
    # 添加日志
    task['logs'].append({
        "time": datetime.datetime.now().isoformat(),
        "action": "恢复任务",
        "detail": f"任务继续执行"
    })
    
    with open(_get_task_path(task_id), 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    # 触发钩子
    trigger_hook(HOOK_ON_TASK_RESUME, task, {"action": "resume"})
    
    return True


# 测试
if __name__ == "__main__":
    from .task import create_task
    
    # 测试创建任务
    task_id = create_task("测试 Tracker + 钩子")
    print(f"创建任务: {task_id}")
    
    # 测试开始任务
    start_task(task_id)
    print("任务已开始")
    
    # 测试记录决策
    add_decision(task_id, "使用 JSON + MD 存储", "避免双存储同步问题")
    print("已记录决策")
    
    # 测试记录问题
    add_problem(task_id, "上下文丢失", "使用 MD 存档解决")
    print("已记录问题")
