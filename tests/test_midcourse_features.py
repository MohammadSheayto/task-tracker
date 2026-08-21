"""Mid-course project tests — due dates + overdue filter, and tags.

Follows the same TestClient + clean-storage pattern as tests/test_tasks.py.
"""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app

client = TestClient(app)

YESTERDAY = (date.today() - timedelta(days=1)).isoformat()
TOMORROW = (date.today() + timedelta(days=1)).isoformat()


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


# --- Feature 1: due dates + overdue filter ---


def test_create_task_with_valid_due_date():
    body = create_task(due_date=TOMORROW)
    assert body["due_date"] == TOMORROW


def test_create_task_without_due_date_defaults_to_null():
    body = create_task()
    assert body["due_date"] is None


def test_create_task_invalid_due_date_returns_422():
    response = client.post("/tasks", json={"title": "x", "due_date": "not-a-date"})
    assert response.status_code == 422
    assert "due_date" in str(response.json()["detail"])


def test_patch_due_date_updates_task():
    task = create_task()
    response = client.patch(f"/tasks/{task['id']}", json={"due_date": TOMORROW})
    assert response.status_code == 200
    assert response.json()["due_date"] == TOMORROW


def test_overdue_filter_returns_only_overdue_tasks():
    overdue_task = create_task(title="Past due", due_date=YESTERDAY)
    create_task(title="Future due", due_date=TOMORROW)
    create_task(title="Past due but Done", due_date=YESTERDAY, status="Done")
    create_task(title="No due date")

    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    ids = [task["id"] for task in response.json()]
    assert ids == [overdue_task["id"]]


def test_overdue_false_filter_excludes_overdue_tasks():
    create_task(title="Past due", due_date=YESTERDAY)
    future = create_task(title="Future due", due_date=TOMORROW)

    response = client.get("/tasks", params={"overdue": "false"})
    assert response.status_code == 200
    ids = [task["id"] for task in response.json()]
    assert future["id"] in ids
    assert len(ids) == 1


# --- Feature 2: tags / labels ---


def test_create_task_with_tags_trims_and_dedupes():
    body = create_task(tags=["  frontend ", "bug", "frontend"])
    assert body["tags"] == ["frontend", "bug"]


def test_create_task_without_tags_defaults_to_empty_list():
    body = create_task()
    assert body["tags"] == []


def test_create_task_blank_tag_returns_422():
    response = client.post("/tasks", json={"title": "x", "tags": ["ok", "   "]})
    assert response.status_code == 422
    assert "blank" in str(response.json()["detail"]).lower()


def test_create_task_too_many_tags_returns_422():
    response = client.post("/tasks", json={"title": "x", "tags": [f"t{i}" for i in range(11)]})
    assert response.status_code == 422
    assert "at most" in str(response.json()["detail"]).lower()


def test_patch_tags_replaces_list():
    task = create_task(tags=["old"])
    response = client.patch(f"/tasks/{task['id']}", json={"tags": ["new-a", "new-b"]})
    assert response.status_code == 200
    assert response.json()["tags"] == ["new-a", "new-b"]


def test_tags_preserved_after_unrelated_patch():
    task = create_task(tags=["keep-me"])
    response = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["tags"] == ["keep-me"]


def test_filter_by_tag_returns_only_matching_tasks():
    tagged = create_task(title="Tagged", tags=["backend"])
    create_task(title="Other tag", tags=["frontend"])
    create_task(title="No tags")

    response = client.get("/tasks", params={"tag": "backend"})
    assert response.status_code == 200
    ids = [task["id"] for task in response.json()]
    assert ids == [tagged["id"]]


def test_filter_by_unknown_tag_returns_empty_list():
    create_task(tags=["backend"])
    response = client.get("/tasks", params={"tag": "nope"})
    assert response.status_code == 200
    assert response.json() == []
