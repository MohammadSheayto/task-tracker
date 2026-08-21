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


MAX_TAGS = 10
MAX_TAG_LENGTH = 30


def _validate_tags(tags: Optional[list[str]]) -> Optional[list[str]]:
    """Trim tags, reject blank/overlong values, dedupe, and cap the count.

    Raises:
        ValueError: If a tag is blank, a tag exceeds MAX_TAG_LENGTH, or
            more than MAX_TAGS distinct tags are provided.
    """
    if tags is None:
        return None
    cleaned: list[str] = []
    for tag in tags:
        tag = tag.strip()
        if not tag:
            raise ValueError("tags must not contain blank values")
        if len(tag) > MAX_TAG_LENGTH:
            raise ValueError(f"each tag must not exceed {MAX_TAG_LENGTH} characters")
        if tag not in cleaned:
            cleaned.append(tag)
    if len(cleaned) > MAX_TAGS:
        raise ValueError(f"a task may have at most {MAX_TAGS} tags")
    return cleaned


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
    tags: list[str] = []

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

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Normalize and validate the tag list."""
        return _validate_tags(v)


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
    tags: Optional[list[str]] = None

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

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Normalize and validate the tag list when provided."""
        return _validate_tags(v)


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
    tags: list[str]
    created_at: datetime
    updated_at: datetime
