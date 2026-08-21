"""Task Tracker API.

FastAPI application per ADR-001. In-memory storage backend with
CRUD endpoints for tasks; CORS enabled for the local Module 3 frontend.
"""

from datetime import date, datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.config import APP_ENV
from app.models import TaskCreate, TaskResponse, TaskStatus, TaskUpdate

app = FastAPI(
    title="Task Tracker API",
    description="Learning project: a REST API for tracking tasks.",
    version="0.2.0",
)

# Allow the local frontend (frontend/index.html served on port 5500,
# e.g. VS Code Live Server or `python -m http.server 5500`) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Liveness check.

    Returns HTTP 200 with the service status and the current UTC
    timestamp in ISO 8601 format.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Request body: TaskCreate with title (required), description, status, priority, assignee.
    Returns: Created task with auto-generated id and UTC timestamps.
    Validation errors (missing/blank/overlong title, invalid enums, unknown fields) return HTTP 422.
    """
    return storage.add_task(payload)


def _is_overdue(task: TaskResponse) -> bool:
    """A task is overdue when its due date has passed and it is not Done."""
    return (
        task.due_date is not None
        and task.due_date < date.today()
        and task.status != TaskStatus.DONE
    )


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(overdue: bool | None = None, tag: str | None = None) -> list[TaskResponse]:
    """List tasks in insertion order.

    Query parameters:
        overdue: If true, return only overdue tasks (due date before today
            and status not Done). If false, return only non-overdue tasks.
            Omit to return all tasks.
        tag: Return only tasks carrying this exact tag.
    """
    tasks = storage.get_all_tasks()
    if overdue is not None:
        tasks = [task for task in tasks if _is_overdue(task) == overdue]
    if tag is not None:
        tasks = [task for task in tasks if tag in task.tags]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by ID.

    Returns HTTP 404 if no task exists with the given ID.
    """
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Only fields present in the request body are changed. Validation
    errors (blank/overlong title, invalid enums, unknown fields) return
    HTTP 422; an unknown task ID returns HTTP 404.
    """
    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by ID.

    Returns HTTP 204 on success, HTTP 404 if the task does not exist.
    """
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")