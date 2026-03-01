"""内存任务存储，管理异步删除任务的生命周期。"""

import asyncio
import uuid
from datetime import datetime
from typing import Optional

from api.models import TaskStatus, TaskResponse


class TaskStore:
    """线程安全的内存任务存储，包含全局删除锁。"""

    def __init__(self):
        self._tasks: dict[str, TaskResponse] = {}
        self._deletion_lock = asyncio.Lock()
        self._active_entities: set[str] = set()

    @property
    def deletion_lock(self) -> asyncio.Lock:
        return self._deletion_lock

    def create_task(self, entity_name: str) -> TaskResponse:
        task_id = uuid.uuid4().hex[:12]
        task = TaskResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            entity_name=entity_name,
            created_at=datetime.now(),
        )
        self._tasks[task_id] = task
        self._active_entities.add(entity_name.lower())
        return task

    def get_task(self, task_id: str) -> Optional[TaskResponse]:
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[TaskResponse]:
        return list(self._tasks.values())

    def is_entity_active(self, entity_name: str) -> bool:
        return entity_name.lower() in self._active_entities

    def mark_running(self, task_id: str):
        task = self._tasks[task_id]
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

    def mark_completed(self, task_id: str, result: dict):
        task = self._tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        self._active_entities.discard(task.entity_name.lower())

    def mark_failed(self, task_id: str, error: str):
        task = self._tasks[task_id]
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.error = error
        self._active_entities.discard(task.entity_name.lower())
