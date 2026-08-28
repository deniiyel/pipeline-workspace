import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    init_db()
    conn = sqlite3.connect("auth.db", timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("DELETE FROM users;")
    conn.commit()
    conn.close()
    yield

def test_register_user():
    res = client.post("/register", json={"username": "daniyal", "password": "securepassword123"})
    assert res.status_code == 201
    assert res.json()["message"] == "User registered successfully"

def test_register_duplicate_username():
    client.post("/register", json={"username": "daniyal", "password": "password123"})
    res = client.post("/register", json={"username": "daniyal", "password": "anotherpassword"})
    assert res.status_code == 400

def test_login_success():
    client.post("/register", json={"username": "daniyal", "password": "securepassword123"})
    res = client.post("/login", json={"username": "daniyal", "password": "securepassword123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_invalid_password():
    client.post("/register", json={"username": "daniyal", "password": "securepassword123"})
    res = client.post("/login", json={"username": "daniyal", "password": "wrongpassword"})
    assert res.status_code == 401

def test_access_protected_route_with_token():
    client.post("/register", json={"username": "daniyal", "password": "securepassword123"})
    login_res = client.post("/login", json={"username": "daniyal", "password": "securepassword123"})
    token = login_res.json()["access_token"]
    res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "daniyal" in res.json()["message"]

def test_access_protected_route_without_token():
    res = client.get("/protected")
    assert res.status_code in (401, 403)