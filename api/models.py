"""Pydantic 请求/响应模型。"""

from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class DeleteRequest(BaseModel):
    entity_name: str = Field(..., min_length=1, description="要删除的实体名称")
    cache_dir: str = Field(default="cache", description="缓存目录路径")
    no_backup: bool = Field(default=False, description="跳过删除前备份")


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    entity_name: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class EntityExistsResponse(BaseModel):
    entity_name: str
    exists: bool
    info: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str = "ok"
    cache_dir_exists: bool
    graphml_exists: bool
