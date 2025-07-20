from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    status: TaskStatus


class TaskInDB(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Task(TaskInDB):
    pass
