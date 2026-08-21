"""In-memory task storage layer — Module 2.

Provides a thread-safe store for task data using a dictionary backend.
Planned migration to SQLite in a future module.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskResponse, TaskUpdate


class TaskStorage:
    """In-memory task store with CRUD operations.

    All task IDs are UUIDs. Timestamps are UTC.
    Not thread-safe; for production use, add locks or move to a database.
    """

    def __init__(self) -> None:
        """Initialize an empty task store."""
        # Internal store: {task_id: {task_data}}
        self._tasks: dict[str, dict] = {}

    def create(self, task_create: TaskCreate) -> TaskResponse:
        """Create a new task.

        Args:
            task_create: Validated task creation request.

        Returns:
            Created task with auto-generated id and timestamps.
        """
        task_id = str(uuid4())
        now = datetime.now(timezone.utc)

        task_data = {
            "id": task_id,
            "title": task_create.title,
            "description": task_create.description or "",
            "status": task_create.status,
            "priority": task_create.priority,
            "assignee": task_create.assignee,
            "created_at": now,
            "updated_at": now,
        }

        self._tasks[task_id] = task_data
        return TaskResponse(**task_data)

    def read(self, task_id: str) -> Optional[TaskResponse]:
        """Retrieve a task by ID.

        Args:
            task_id: The UUID of the task.

        Returns:
            Task data if found, None otherwise.
        """
        if task_id not in self._tasks:
            return None
        return TaskResponse(**self._tasks[task_id])

    def read_all(self) -> list[TaskResponse]:
        """Retrieve all tasks.

        Returns:
            List of all tasks in insertion order.
        """
        return [TaskResponse(**task_data) for task_data in self._tasks.values()]

    def update(self, task_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update a task's editable fields.

        Args:
            task_id: The UUID of the task.
            task_update: Partial update request.

        Returns:
            Updated task if found, None otherwise.

        Note:
            Only updates fields that are explicitly provided (not None).
            Automatically updates the updated_at timestamp.
        """
        if task_id not in self._tasks:
            return None

        task_data = self._tasks[task_id]

        # Update only provided fields
        if task_update.title is not None:
            task_data["title"] = task_update.title
        if task_update.description is not None:
            task_data["description"] = task_update.description
        if task_update.status is not None:
            task_data["status"] = task_update.status
        if task_update.priority is not None:
            task_data["priority"] = task_update.priority
        if task_update.assignee is not None:
            task_data["assignee"] = task_update.assignee

        # Always update the updated_at timestamp
        task_data["updated_at"] = datetime.now(timezone.utc)

        return TaskResponse(**task_data)

    def delete(self, task_id: str) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The UUID of the task.

        Returns:
            True if the task was deleted, False if not found.
        """
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True


# Module-level instance
_store = TaskStorage()


# Public API functions
def add_task(task_create: TaskCreate) -> TaskResponse:
    """Create a new task."""
    return _store.create(task_create)


def get_task(task_id: str) -> Optional[TaskResponse]:
    """Retrieve a task by ID."""
    return _store.read(task_id)


def get_all_tasks() -> list[TaskResponse]:
    """Retrieve all tasks."""
    return _store.read_all()


def update_task(task_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
    """Update a task."""
    return _store.update(task_id, task_update)


def delete_task(task_id: str) -> bool:
    """Delete a task."""
    return _store.delete(task_id)


def clear_tasks() -> None:
    """Remove all tasks. Intended for test isolation."""
    _store._tasks.clear()
