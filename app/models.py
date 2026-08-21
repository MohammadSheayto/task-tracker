"""Pydantic models for Task Tracker API — Module 2.

Defines data models and validation rules for task operations.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    """Task lifecycle states."""

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    """Task importance levels."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    """Request model for creating a new task.

    Validates input and sets sensible defaults for optional fields.
    """

    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Strip whitespace and validate title length.

        Raises:
            ValueError: If title is blank or exceeds 200 characters.
        """
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must not exceed 200 characters")
        return v


class TaskUpdate(BaseModel):
    """Request model for updating an existing task.

    All fields are optional. Omitted fields are not updated.
    """

    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace and validate title length when provided.

        Raises:
            ValueError: If title is blank or exceeds 200 characters.
        """
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must not exceed 200 characters")
        return v


class TaskResponse(BaseModel):
    """Response model for task operations.

    Includes read-only metadata (id, timestamps).
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
