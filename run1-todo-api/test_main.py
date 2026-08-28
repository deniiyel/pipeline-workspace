import pytest
from fastapi.testclient import TestClient
from main import app, init_db
import sqlite3

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    init_db()
    conn = sqlite3.connect("tasks.db")
    conn.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()

def test_create_task():
    res = client.post("/tasks", json={"title": "Test Task", "description": "Pytest verification"})
    assert res.status_code == 201
    assert res.json()["title"] == "Test Task"

def test_get_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_get_single_task():
    create_res = client.post("/tasks", json={"title": "Unique Task"})
    task_id = create_res.json()["id"]
    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Unique Task"

def test_get_nonexistent_task():
    res = client.get("/tasks/9999")
    assert res.status_code == 404

def test_create_task_empty_title():
    res = client.post("/tasks", json={"title": "   "})
    assert res.status_code == 400

def test_delete_task():
    create_res = client.post("/tasks", json={"title": "To Delete"})
    task_id = create_res.json()["id"]
    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 204

def test_delete_nonexistent_task():
    res = client.delete("/tasks/9999")
    assert res.status_code == 404