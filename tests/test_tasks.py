"""API tests for the Task Tracker — POST /tasks and PATCH /tasks/{id}.

Uses FastAPI's TestClient against the in-memory storage backend.
Storage is cleared around every test so tests stay independent.
"""

import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    """Reset the in-memory store before and after each test."""
    storage.clear_tasks()
    yield
    storage.clear_tasks()


def create_task(**overrides) -> dict:
    """Create a task through the API and return the response body."""
    payload = {"title": "Sample task", **overrides}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


# --- POST /tasks ---


def test_create_task_returns_201_with_defaults():
    body = create_task()
    assert body["title"] == "Sample task"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["description"] == ""
    assert body["assignee"] is None
    assert body["id"]


def test_create_task_blank_title_returns_422():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422
    assert "title" in str(response.json()["detail"]).lower()


def test_create_task_invalid_status_returns_422():
    response = client.post("/tasks", json={"title": "x", "status": "Archived"})
    assert response.status_code == 422


# --- GET /tasks ---


def test_list_tasks_returns_created_tasks():
    first = create_task(title="First")
    second = create_task(title="Second")
    response = client.get("/tasks")
    assert response.status_code == 200
    ids = [task["id"] for task in response.json()]
    assert ids == [first["id"], second["id"]]


def test_get_task_unknown_id_returns_404():
    response = client.get("/tasks/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# --- PATCH /tasks/{id} ---


def test_patch_status_updates_task():
    task = create_task()
    response = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_partial_update_preserves_other_fields():
    task = create_task(title="Keep me", priority="High", assignee="Mohammad")
    response = client.patch(f"/tasks/{task['id']}", json={"description": "New details"})
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "New details"
    assert body["title"] == "Keep me"
    assert body["priority"] == "High"
    assert body["assignee"] == "Mohammad"


def test_patch_blank_title_returns_422():
    task = create_task()
    response = client.patch(f"/tasks/{task['id']}", json={"title": "   "})
    assert response.status_code == 422
    assert "title" in str(response.json()["detail"]).lower()


def test_patch_invalid_status_returns_422():
    task = create_task()
    response = client.patch(f"/tasks/{task['id']}", json={"status": "Whatever"})
    assert response.status_code == 422


def test_patch_unknown_field_returns_422():
    task = create_task()
    response = client.patch(f"/tasks/{task['id']}", json={"made_up": "value"})
    assert response.status_code == 422


def test_patch_unknown_id_returns_404():
    response = client.patch("/tasks/does-not-exist", json={"status": "Done"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# --- DELETE /tasks/{id} ---


def test_delete_task_then_get_returns_404():
    task = create_task()
    delete_response = client.delete(f"/tasks/{task['id']}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 404
